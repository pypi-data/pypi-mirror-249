import random
import re
import string
import subprocess
from pathlib import Path
from shutil import rmtree
from textwrap import dedent

import click

from dfu.config import Config
from dfu.installed_packages.pacman import diff_packages, get_installed_packages
from dfu.package.dfu_diff import DfuDiff
from dfu.package.package_config import PackageConfig
from dfu.revision.git import (
    git_add,
    git_check_ignore,
    git_checkout,
    git_current_branch,
    git_default_branch,
    git_delete_branch,
    git_diff,
    git_ls_files,
    git_reset_branch,
    git_stash,
    git_stash_pop,
)
from dfu.snapshots.snapper import Snapper


def begin_diff(config: Config, package_dir: Path):
    dfu_diff_path = package_dir / '.dfu-diff'
    diff = DfuDiff()
    try:
        diff.write(dfu_diff_path, mode="x")
    except FileExistsError:
        raise ValueError("A diff is already in progress. Run `dfu diff --continue` to continue the diff.")
    continue_diff(config, package_dir)


def abort_diff(package_dir: Path):
    click.echo("Cleaning up...", err=True)
    _rmtree(package_dir, 'placeholders')
    _rmtree(package_dir, 'files')
    try:
        diff = DfuDiff.from_file(package_dir / '.dfu-diff')
    except FileNotFoundError:
        # The diff file doesn't exist, so there's nothing to abort
        return

    git_checkout(package_dir, git_default_branch(package_dir), exist_ok=True)
    if diff.base_branch:
        git_delete_branch(package_dir, diff.base_branch)

    if diff.target_branch:
        git_delete_branch(package_dir, diff.target_branch)

    (package_dir / '.dfu-diff').unlink(missing_ok=True)


def continue_diff(config: Config, package_dir: Path):
    diff = DfuDiff.from_file(package_dir / '.dfu-diff')
    if not diff.created_placeholders:
        click.echo("Creating placeholder files...", err=True)
        create_changed_placeholders(package_dir)
        diff.created_placeholders = True
        diff.write(package_dir / '.dfu-diff')
        click.echo(
            dedent(
                """\
                Placeholder files have been created. Run `git ls-files --others placeholders` to see them.
                If there are extra files, delete them. Do not git commit anything in placeholders.
                Once completed, run `dfu diff --continue`."""
            ),
            err=True,
        )
        return

    if not diff.base_branch:
        create_base_branch(package_dir, diff)
        click.echo(
            dedent(
                """\
                The files/ directory is now populated with the contents at the time of `dfu begin`
                Make sure all the files here are what you wish to track. Then, commit ONLY the files/ directory to this base branch.
                After you've git committed any changes to the base branch, run `dfu diff --continue`."""
            ),
            err=True,
        )
        return

    if not diff.target_branch:
        create_target_branch(package_dir, diff)
        click.echo(
            dedent(
                """\
                The files/ directory is now populated with the contents at the time of `dfu end`
                This represents the git diff for the files that were changed between the two snapshots.
                Double-check that the final git diff is correct. If it is, commit ONLY the files/ directory to this target branch.
                After you've git committed any changes to the target branch, run `dfu diff --continue`."""
            ),
            err=True,
        )
        return

    default_branch = git_default_branch(package_dir)
    click.echo(f"Checking out the {default_branch} branch", err=True)
    git_checkout(package_dir, default_branch, exist_ok=True)

    if not diff.created_patch_file:
        create_patch_file(package_dir, diff)
        diff.created_patch_file = True
        diff.write(package_dir / '.dfu-diff')
        click.echo("Created the changes.patch file", err=True)

    if not diff.updated_installed_programs:
        click.echo("Detecting which programs were installed and removed...", err=True)
        update_installed_packages(config, package_dir)
        diff.updated_installed_programs = True
        diff.write(package_dir / '.dfu-diff')
        click.echo("Updated the installed programs", err=True)

    click.echo("Deleting the temporary base and target branches...", err=True)
    update_primary_branches(package_dir, diff)
    abort_diff(package_dir)


def update_installed_packages(config: Config, package_dir: Path):
    package_config = PackageConfig.from_file(package_dir / "dfu_config.json")
    if len(package_config.snapshots) == 0:
        raise ValueError('Did not create a successful pre/post snapshot pair')
    old_packages = get_installed_packages(config, package_config.snapshot_mapping(use_pre_id=True))
    new_packages = get_installed_packages(config, package_config.snapshot_mapping(use_pre_id=False))

    diff = diff_packages(old_packages, new_packages)
    package_config.programs_added = diff.added
    package_config.programs_removed = diff.removed
    package_config.write(package_dir / "dfu_config.json")


def create_changed_placeholders(package_dir: Path):
    package_config = PackageConfig.from_file(package_dir / "dfu_config.json")
    # This method has been performance optimized in several places. Take care when modifying the file for both correctness and speed
    pre_mapping = package_config.snapshot_mapping(use_pre_id=True)
    post_mapping = package_config.snapshot_mapping(use_pre_id=False)

    _rmtree(package_dir, 'placeholders')
    placeholder_dir = package_dir / 'placeholders'

    placeholder_dir.mkdir(mode=0o755, parents=True, exist_ok=True)
    for snapper_name, pre_id in pre_mapping.items():
        post_id = post_mapping[snapper_name]
        snapper = Snapper(snapper_name)
        deltas = snapper.get_delta(pre_id, post_id)

        # Cumulatively, it's expensive to create files, so we want to filter out .gitignore files and skip writing them
        # git_check_ignore will return a list of all the paths that are ignored by git, but we need to be careful about the path
        # As far as git is concerned, the path should be placeholders/<path>, so we will set that once here
        # And then the code to actually write the file joins it with package_dir later
        for delta in deltas:
            delta.path = f"placeholders/{delta.path.lstrip('/')}"

        # Create a set of all the ignored files. Earlier attempts tried using a list and checking the last element, but the ordering wasn't exact
        ignored_paths = set(git_check_ignore(package_dir, [delta.path for delta in deltas]))
        for delta in deltas:
            if delta.path in ignored_paths:
                # Performance speedup: Don't write files that are ignored by git
                continue
            path = package_dir / delta.path
            try:
                # Performance speedup: Try calling mkdir once, to create all of the parent directories
                path.parent.mkdir(parents=True, exist_ok=True, mode=0o755)
            except FileExistsError:
                # Calling mkdir() doesn't work in all cases, because sometimes we mistakenly create a file, instead of a directory
                # diff_packages doesn't distinguish between files and directories, so the placeholder algorithm assumes they're always files
                # Therefore, we may have previously created a parent directory as a file. So, we need to manually walk the path
                # Delete any placeholder files that are actually directories, and re-create them as directories
                # This is the slow path, so only do it if there are conflicts
                current_path = Path(path.parts[0])
                for child in path.parts[1:-1]:
                    current_path = current_path / child

                    if current_path.is_file():
                        current_path.unlink()
                        current_path.mkdir(mode=0o755)
                    elif not current_path.exists():
                        current_path.mkdir(mode=0o755)
                    elif not current_path.is_dir():
                        raise ValueError(f"Trying to create {path} failed because {current_path} is not a directory")

            path.write_text(f"PLACEHOLDER: {delta.action}\n")


def copy_files(package_dir: Path, *, use_pre_id: bool):
    package_config = PackageConfig.from_file(package_dir / "dfu_config.json")
    _rmtree(package_dir, 'files')
    for snapper_name, snapshot_id in package_config.snapshot_mapping(use_pre_id=use_pre_id).items():
        snapper = Snapper(snapper_name)
        ls_dir = package_dir / 'placeholders' / _strip_placeholders(snapper.get_mountpoint())
        try:
            files_to_copy = [_strip_placeholders(f) for f in git_ls_files(ls_dir)]
        except FileNotFoundError:
            # The ls_dir doesn't exist, so there are no placeholders to copy
            continue
        snapshot_dir = snapper.get_snapshot_path(snapshot_id)
        for file in files_to_copy:
            src = snapshot_dir / file
            dest = package_dir / 'files' / file
            dest.parent.mkdir(mode=0o755, parents=True, exist_ok=True)

            if subprocess.run(['sudo', 'stat', str(src)], capture_output=True).returncode == 0:
                subprocess.run(
                    ['sudo', 'cp', '--no-dereference', '--preserve=all', str(src), str(dest)],
                    capture_output=True,
                    check=True,
                )


def create_base_branch(package_dir: Path, diff: DfuDiff):
    branch_name = f"base-{_rand_slug()}"
    click.echo(f"Creating base branch {branch_name}...", err=True)
    git_checkout(package_dir, branch_name, exist_ok=False)
    copy_files(package_dir, use_pre_id=True)
    git_add(package_dir, ['files'])
    diff.base_branch = branch_name
    diff.write(package_dir / '.dfu-diff')


def create_target_branch(package_dir: Path, diff: DfuDiff):
    if diff.base_branch is None:
        raise ValueError('Cannot create target branch without a base branch')
    git_checkout(package_dir, diff.base_branch, exist_ok=True)

    branch_name = f"target-{_rand_slug()}"
    click.echo(f"Creating target branch {branch_name}...", err=True)
    git_checkout(package_dir, branch_name, exist_ok=False)
    copy_files(package_dir, use_pre_id=False)
    git_add(package_dir, ['files'])
    diff.target_branch = branch_name
    diff.write(package_dir / '.dfu-diff')


def create_patch_file(package_dir: Path, diff: DfuDiff):
    if diff.base_branch is None or diff.target_branch is None:
        raise ValueError('Cannot create a patch file without a base and target branch')
    patch = git_diff(package_dir, diff.base_branch, diff.target_branch)
    (package_dir / 'changes.patch').write_text(patch)


def update_primary_branches(package_dir: Path, diff: DfuDiff):
    git_add(package_dir, [package_dir])
    current_branch = git_current_branch(package_dir)
    git_stash(package_dir)
    if diff.base_branch is None or diff.target_branch is None:
        raise ValueError('Cannot update primary branches without a base and target branch')

    git_checkout(package_dir, diff.base_branch, exist_ok=True)
    git_checkout(package_dir, "base", exist_ok=True)
    git_reset_branch(package_dir, diff.base_branch)

    git_checkout(package_dir, "target", exist_ok=True)
    git_reset_branch(package_dir, diff.target_branch)

    git_checkout(package_dir, current_branch, exist_ok=True)
    git_stash_pop(package_dir)


def _rmtree(package_dir: Path, subdir: str):
    placeholder_dir = package_dir / subdir
    if placeholder_dir.exists():
        rmtree(placeholder_dir)


def _strip_placeholders(p: Path | str) -> str:
    return re.sub(r'^placeholders/', '', str(p)).lstrip('/')


def _rand_slug(length=10):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
