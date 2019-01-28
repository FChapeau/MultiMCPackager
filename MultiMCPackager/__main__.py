import click
import pathlib
import shutil
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

    if not (instancepath / "instance.cfg").exists():
        # TODO find more elegant way to abort program execution
        raise Exception("Not a MultiMC Instance")

    outputpath.mkdir(exist_ok=True)
    (outputpath / "mods").mkdir(exist_ok=True)

    click.echo("Copying mods")
    with click.progressbar(iterable=(instancepath / ".minecraft"/ "mods").glob("*.jar")) as bar:
        for child in bar:
            if not (server and "clientonly" in child.name):
                shutil.copyfile(child, outputpath / "mods" / child.name)

    click.echo("Copying config")
    if not (outputpath / "config").exists():
        shutil.copytree(instancepath / ".minecraft" / "config", outputpath / "config", )

    instance = Instance(instancepath)
    print(instance.name)
    print(instance.forge_version)
    print(instance.minecraft_version)

if __name__ == "__main__":
    main()
