import os
import sys
from pathlib import Path

import click

from dfu.commands import (
    abort_diff,
    begin_diff,
    continue_diff,
    create_config,
    create_distribution,
    create_package,
    create_post_snapshot,
    create_pre_snapshot,
    get_config_paths,
    load_config,
)
from dfu.config import Config
from dfu.package.package_config import find_package_config
from dfu.snapshots.snapper import Snapper


class NullableString(click.ParamType):
    name = "string"

    def convert(self, value, param, ctx):
        if value == "":
            return None
        return value


def find_package_dir(path: Path = Path.cwd()) -> Path:
    config_path = find_package_config(path)
    if not config_path:
        raise ValueError("No dfu_config.json found in the current directory or any parent directory")
    return config_path.parent


@click.group()
def main():
    pass


@main.command()
@click.option("-n", "--name", help="Name of the package")
@click.option("-d", "--description", help="Description of the package")
def init(name: str | None, description: str | None):
    final_name: str = click.prompt("Name", default=name or Path.cwd().name)
    final_description: str | None = click.prompt("Description", default=description or "", type=NullableString())
    path = create_package(name=final_name, description=final_description)
    print(path)


@main.command()
def begin():
    config = load_config()
    package_dir = find_package_dir()
    create_pre_snapshot(config, package_dir)


@main.command()
def end():
    package_dir = find_package_dir()
    create_post_snapshot(package_dir)


@main.command()
@click.option('--abort', is_flag=True, help='Abort the operation', default=None)
@click.option('--continue', 'continue_', is_flag=True, help='Continue the rebase operation', default=None)
def diff(abort: bool | None, continue_: bool | None):
    if abort and continue_:
        raise ValueError("Cannot specify both --abort and --continue")
    config = load_config()
    package_dir = find_package_dir()
    if abort:
        abort_diff(package_dir)
    elif continue_:
        continue_diff(config, package_dir)
    else:
        begin_diff(config, package_dir)


@main.command()
def dist():
    package_dir = find_package_dir()
    create_distribution(package_dir)


@click.group
def config():
    pass


@config.command(name="init")
@click.option("-s", "--snapper-config", multiple=True, default=[], help="Snapper configs to include")
@click.option("-f", "--file", help="File to write config to")
def config_init(snapper_config: list[str], file: str | None):
    if not snapper_config:
        default_configs = ",".join([c.name for c in Snapper.get_configs()])
        response = click.prompt(
            "Which snapper configs would you like to create snapshots for?",
            default=default_configs,
        )
        snapper_config = [c.strip() for c in response.split(",") if c.strip()]
    if file is None:
        file = str(click.prompt("Where would you like to store the dfu config?", default=get_config_paths()[0]))
    create_config(file=Path(file), snapper_configs=snapper_config)


main.add_command(config)


if __name__ == "__main__":
    if os.geteuid() == 0:
        click.echo("Don't run dfu as root")
        sys.exit(1)
    main()
