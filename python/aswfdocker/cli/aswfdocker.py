import os
import logging
import subprocess
import click

from aswfdocker import builder, migrater, buildinfo, constants, utils


logger = logging.getLogger("build-images")


pass_build_info = click.make_pass_decorator(buildinfo.BuildInfo)


@click.group()
@click.option(
    "--repo-root",
    "-r",
    envvar="ASWF_REPO_ROOT",
    default=".",
    help="Root of aswf-docker repository",
)
@click.option("--repo-uri", "-u", help="URL of current Git Repository")
@click.option("--source-branch", "-b", help="Current git branch name")
@click.option("--verbose", "-v", is_flag=True, help="Enables verbose mode.")
@click.version_option("1.0")
@click.pass_context
def cli(ctx, repo_root, repo_uri, source_branch, verbose):
    """aswfdocker is a command line interface to build ASWF Docker packages and ci images
    """
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    ctx.obj = buildinfo.BuildInfo(
        repo_uri=repo_uri,
        source_branch=source_branch,
        repo_root=os.path.abspath(repo_root),
    )


@cli.command()
@click.option(
    "--ci-image-type",
    "-t",
    required=True,
    help="Builds a ci-package or a ci-image.",
    type=click.Choice(constants.IMAGE_TYPE.__members__.keys(), case_sensitive=True),
)
@click.option(
    "--group-name",
    "-g",
    required=True,
    help='The name of the group of images to build, e.g. "base" or "vfx".',
)
@click.option(
    "--group-version",
    "-v",
    required=True,
    help='The major version number to build, e.g. "2019".',
)
@click.option(
    "--target",
    "-tg",
    required=False,
    help='An optional package or image name to build, e.g. "usd".',
)
@click.option(
    "--push", "-p", is_flag=True, help="Push built images to docker repository."
)
@click.option("--dry-run", "-d", is_flag=True, help="Just logs what would happen.")
@click.option(
    "--progress",
    "-pr",
    type=click.Choice(("auto", "tty", "plain"), case_sensitive=True),
    default="auto",
    help='Set type of progress output for "docker buildx bake" command.',
)
@pass_build_info
def build(
    build_info,
    ci_image_type,
    group_name,
    group_version,
    target,
    push,
    dry_run,
    progress,
):
    """Builds a ci-package or ci-image docker image.
    """
    b = builder.Builder(
        build_info=build_info,
        image_type=constants.IMAGE_TYPE[ci_image_type],
        group_name=group_name,
        group_version=group_version,
        target=target,
        push=push,
    )
    b.build(dry_run=dry_run, progress=progress)


@cli.command()
@click.option("--from", "-f", "from_org", default="aswftesting")
@click.option("--to", "-t", "to_org", default="aswf")
@click.option(
    "--package",
    "-p",
    help="Optional package name to migrate (all packages are migrated by default)",
)
@click.option(
    "--version",
    "-v",
    help="Version of the package to migrate (all versions are migrated by default)",
)
@click.option("--dry-run", "-d", is_flag=True)
def migrate(from_org, to_org, package, version, dry_run):
    m = migrater.Migrater(from_org, to_org)
    m.gather(package, version)
    if not click.confirm(
        "Are you sure you want to migrate the following {} packages?\n{}\n".format(
            len(m.migration_list),
            "\n".join("{} -> {}".format(f, t) for f, t in m.migration_list),
        )
    ):
        return
    m.migrate(dry_run)


@cli.command()
@pass_build_info
def getdockerorg(build_info):
    click.echo(utils.get_docker_org(build_info.repo_uri, build_info.source_branch))


@cli.command()
@pass_build_info
def getdockerpush(build_info):
    click.echo(utils.get_docker_push(build_info.repo_uri, build_info.source_branch))
