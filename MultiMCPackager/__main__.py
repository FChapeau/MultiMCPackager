import click
import pathlib
import shutil


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

    for child in (instancepath / ".minecraft"/ "mods").glob("*.jar"):
        if not (server and "clientonly" in child.name):
            shutil.copyfile(child, outputpath / "mods" / child.name)

    if not (outputpath / "config").exists():
        shutil.copytree(instancepath / ".minecraft" / "config", outputpath / "config", )


if __name__ == "__main__":
    main()
