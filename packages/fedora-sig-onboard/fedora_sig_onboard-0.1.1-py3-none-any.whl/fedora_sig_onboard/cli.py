# SPDX-License-Identifier: MIT

from pathlib import Path
import os
import sys

import click
from xdg import BaseDirectory

from .onboarder import Onboarder


def fail(msg, retcode=1):
    click.echo(msg, err=True)
    sys.exit(retcode)


@click.group()
@click.option(
    "-c", "--config", type=click.Path(exists=True, dir_okay=False, path_type=Path)
)
@click.option("-d", "--debug", is_flag=True)
@click.pass_context
def cli(ctx, config, debug):
    """Onboard a package onto a SIG"""

    if config is None:
        xdg_dir = BaseDirectory.load_first_config("fedora-sig-onboard")
        if xdg_dir is not None and Path(xdg_dir, "fedora-sig-onboard.conf").exists():
            config = Path(xdg_dir, "fedora-sig-onboard.conf")
        else:
            fail("Invalid or missing config")

    if debug:
        click.echo(f"Using config: {str(config.resolve())}")

    ctx.obj = Onboarder(str(config.resolve()))


pass_onboarder = click.make_pass_decorator(Onboarder, ensure=True)


@cli.command()
@click.option("-g", "--group", help="Group ACL to add")
@click.option(
    "-a",
    "--acl",
    help="Which ACL to give the SIG's group",
    default="commit",
    show_default=True,
    type=click.Choice(["commit", "admin"]),
)
@click.option(
    "-B",
    "--no-set-bz",
    "set_bz",
    help="Don't override Bugzilla assignee to the SIG.",
    is_flag=True,
    default=True,
)
@click.option(
    "-R",
    "--no-set-relmon",
    "set_relmon",
    help="Don't add to release monitoring.",
    is_flag=True,
    default=True,
)
@click.argument("package", required=False, nargs=-1)
@pass_onboarder
def onboard(onboarder, group, acl, set_bz, set_relmon, package):
    if not package:
        package = [Path(os.getcwd()).name]

    for p in package:
        info = onboarder.get_package_info(p)
        if not info:
            fail(f"{p} is not a valid package")

        if not group:
            if p.startswith("golang-"):
                group = "go-sig"
            elif p.startswith("python-"):
                group = "python-packagers-sig"
            elif p.startswith("rust-"):
                group = "rust-sig"
            else:
                fail(f"Could not determine group for {p}")

        click.echo(f"[{p}] updating ACL")
        onboarder.add_package_acl(p, group, acl)
        if group in ["go-sig", "rust-sig"] and set_bz:
            click.echo(f"[{p}] updating Bugzilla assignees")
            onboarder.set_bugzilla_assignee(p, group)
        if group in ["python-packagers-sig", "rust-sig"] and set_relmon:
            click.echo(f"[{p}] adding to release monitoring")
            onboarder.add_package_to_anitya(p)


@cli.command()
@click.option("-p", "--pattern", help="Pattern to filter for")
@pass_onboarder
def packages(onboarder, pattern):
    for p in onboarder.get_packages(pattern):
        click.echo(p["name"])


if __name__ == "__main__":
    cli()
