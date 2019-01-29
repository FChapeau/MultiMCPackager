import click
import pathlib
import shutil
import sys
from MultiMCPackager.instance import Instance


@click.group()
@click.pass_context
def main(ctx):
    pass


@main.command()
@click.option("--server", default=False,help="Includes client-side mods or not", is_flag=True)
@click.option("--output", "-o", help="Package output dir", default="./package", type=click.Path(exists=False, file_okay=False, resolve_path=True))
@click.argument("instancepathstr", metavar="INSTANCE", nargs=1, type=click.Path(exists=True, file_okay=False, resolve_path=True))
@click.pass_context
def package(ctx, server, instancepathstr, output):
    instancepath = pathlib.Path(instancepathstr)
    outputpath = pathlib.Path(output)
    outputpath.mkdir(exist_ok=True)

    if not (instancepath / "instance.cfg").exists():
        click.echo("This is not a MultiMC instance")
        sys.exit(1)

    click.echo("Initializing MultiMC instance")
    instance = Instance(instancepath)

    instance.copy_mods(outputpath/"mods", server)
    instance.copy_config(outputpath/"config")

    if server:
        instance.fetch_forge(outputpath/"forge.jar")
    else:
        instance.fetch_forge(outputpath/"bin"/"modpack.jar")


if __name__ == "__main__":
    main()
