from MultiMCPackager.mod import Mod
from pathlib import Path
import json
import urllib.request
import click
import shutil


class Instance(object):
    def __init__(self, path):
        self.instance_path = Path(path)

        with open(self.instance_path / "instance.cfg") as f:
            lines = f.readlines()
            self.config = dict()
            for line in lines:
                key, value = line.split("=")
                self.config[key] = value.replace("\n", "")

        with open(self.instance_path / "mmc-pack.json") as f:
            pack = json.load(f)
            for component in pack["components"]:
                if component["cachedName"] == "Forge":
                    self.forge_version = component["version"]
                elif component["cachedName"] == "Minecraft":
                    self.minecraft_version = component["version"]

        #self._loadModList(self.instance_path)

    def _loadModList(self, path:Path):
        self.mods = list()

        for file in path.glob(".minecraft/mods/*.jar"):
            self.mods.append(Mod(file))

    @property
    def name(self) -> str:
        return self.config["name"]

    def fetch_forge(self, destination: Path):
        forge_fetch_url = f"https://files.minecraftforge.net/maven/net/minecraftforge/forge/{self.minecraft_version}-{self.forge_version}/forge-{self.minecraft_version}-{self.forge_version}-universal.jar"
        destination.parents[0].mkdir(parents=True, exist_ok=True)

        if destination.exists():
            destination.unlink()

        print("Fetching forge")
        urllib.request.urlretrieve(forge_fetch_url, destination)

    def fetch_minecraft(self, destination: Path):
        pass

    def copy_mods(self, destination: Path, server: bool):
        destination.mkdir(exist_ok=True)

        click.echo("Copying mods")
        with click.progressbar(iterable=(self.instance_path / ".minecraft" / "mods").glob("*.jar")) as bar:
            for child in bar:
                if not (server and "clientonly" in child.name):
                    shutil.copyfile(child, destination / child.name)

    def copy_config(self, destination: Path):
        click.echo("Copying config")
        if not (destination).exists():
            shutil.copytree(self.instance_path / ".minecraft" / "config", destination )