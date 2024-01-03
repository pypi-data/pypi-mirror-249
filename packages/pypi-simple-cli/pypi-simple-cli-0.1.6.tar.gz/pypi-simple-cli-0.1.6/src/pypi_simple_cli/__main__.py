import enum
import os
import re
from typing import List, Optional

import click
from packaging.version import InvalidVersion, Version, parse
from pypi_simple import PyPISimple


class ReleaseStage(enum.IntEnum):
    all = 0
    dev = 1
    alpha = 2
    beta = 3
    rc = 4
    final = 5


@click.group()
@click.option(
    "--endpoint", "-e", help="The base URL of the simple API instance to query"
)
@click.option(
    "--release-stage",
    "-s",
    type=click.Choice(
        list(i.name for i in ReleaseStage),
        case_sensitive=False,
    ),
    default="all",
    help="Lowest release stage",
)
@click.option("--pattern", "-p", help="Use python regex to match the version.")
@click.pass_context
def main(ctx, endpoint, release_stage, pattern):
    ctx.ensure_object(dict)
    endpoint = os.getenv("PIP_INDEX_URL", endpoint)

    if endpoint is None:
        simple = PyPISimple()
    else:
        simple = PyPISimple(endpoint=endpoint)

    ctx.obj["simple"] = simple
    ctx.obj["release_stage"] = release_stage
    ctx.obj["pattern"] = pattern


def parse_version(version: str) -> Optional[Version]:
    try:
        return parse(version)
    except InvalidVersion:
        return None


def filter_versions(
    ctx: click.core.Context, package: str, version_prefix: Optional[str]
) -> List[str]:
    with ctx.obj["simple"] as client:
        page = client.get_project_page(package)

    if page.versions:
        versions = page.versions
    else:
        raw_versions = (pkg.version or pkg.filename for pkg in page.packages)
        valid_versions = (v for v in raw_versions if parse_version(v) is not None)
        versions = sorted(valid_versions, key=parse_version)
    if version_prefix:
        versions = (v for v in versions if v.startswith(version_prefix))
    release_stage = ReleaseStage[ctx.obj["release_stage"].lower()]
    if release_stage > ReleaseStage.dev:
        versions = (v for v in versions if Version(v).is_devrelease is False)
    if release_stage.value > ReleaseStage.alpha:
        versions = (
            v for v in versions if Version(v).pre is None or Version(v).pre[0] != "a"
        )
    if release_stage.value > ReleaseStage.beta:
        versions = (
            v for v in versions if Version(v).pre is None or Version(v).pre[0] != "b"
        )
    if release_stage.value > ReleaseStage.rc:
        versions = (v for v in versions if Version(v).is_prerelease is False)

    pattern = ctx.obj["pattern"]
    if pattern:
        versions = (v for v in versions if re.search(pattern, v))
    return list(versions)


@click.command("list")
@click.argument("package")
@click.argument("version_prefix", required=False)
@click.pass_context
def list_versions(ctx, package, version_prefix):
    versions = filter_versions(ctx, package, version_prefix)

    for version in versions:
        print(version)


@click.command("latest")
@click.argument("package")
@click.argument("version_prefix", required=False)
@click.pass_context
def latest_version(ctx, package, version_prefix):
    versions = list(filter_versions(ctx, package, version_prefix))
    if len(versions) >= 1:
        print(versions[-1], end="")


main.add_command(list_versions)
main.add_command(latest_version)


if __name__ == "__main__":
    main(obj={})
