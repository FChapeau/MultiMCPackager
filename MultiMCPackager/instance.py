from MultiMCPackager.mod import Mod
from pathlib import Path
import json
import urllib.request
import click
import shutil


class Instance(object):
    """
    Represents a MultiMC instance
    """

    def __init__(self, path):
        """
        Default constructor, requires the path to the instance
        :param path: Path to the instance
        """
        self.instance_path = Path(path)

        with open(self.instance_path / "instance.cfg") as f:
            lines = f.readlines()
            self.config = dict()
            for line in lines:
                if "JvmArgs=" not in line:
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
        """
        Fetch Minecraft Forge jar
        :param destination: Where to send the forge jar file
        """

        forge_fetch_url = f"https://files.minecraftforge.net/maven/net/minecraftforge/forge/{self.minecraft_version}-{self.forge_version}/forge-{self.minecraft_version}-{self.forge_version}-universal.jar"
        destination.parents[0].mkdir(parents=True, exist_ok=True)

        if destination.exists():
            destination.unlink()

        print(f"Fetching forge {self.forge_version}")
        urllib.request.urlretrieve(forge_fetch_url, destination)

    def fetch_minecraft(self, destination: Path, server: bool = True):
        """
        Fetch Minecraft executable jar from the CDN
        :param destination: Where to send the downloaded file
        :param server: Wether to fetch the server or client executable
        """

        # Fetch version manifest
        # https://launchermeta.mojang.com/mc/game/version_manifest.json
        click.echo(f"Fetching Minecraft {self.minecraft_version}")
        with urllib.request.urlopen("https://launchermeta.mojang.com/mc/game/version_manifest.json") as url:
            version_manifest = json.loads(url.read().decode())
            versionlist: list = version_manifest.get("versions")
            version = next((item for item in versionlist if item["id"] == self.minecraft_version))
            versionurl = version["url"]

        # Fetch version specific information

        with urllib.request.urlopen(versionurl) as url:
            manifest = json.loads(url.read().decode())
            jarurl = manifest["downloads"]["server" if server else "client"]["url"]

        # Fetch server jar based on that
        urllib.request.urlretrieve(jarurl, destination)

    def copy_mods(self, destination: Path, server: bool):
        """
        Copies the mod folder to the destination folder

        If the server argument is true, it excludes clientonly mods
        :param destination: Destination where the mods will be sent
        :param server: Toggle telling wether the modpack is for a server or not=
        """
        destination.mkdir(exist_ok=True)

        click.echo("Copying mods")
        with click.progressbar(iterable=(self.instance_path / ".minecraft" / "mods").glob("*.jar")) as bar:
            for child in bar:
                if not (server and "clientonly" in child.name):
                    shutil.copyfile(child, destination / child.name)


    def copy_config(self, destination: Path):
        """
        Copies the mod config folder
        :param destination: Destination where the config will be sent
        """
        click.echo("Copying config")
        if not (destination).exists():
            shutil.copytree(self.instance_path / ".minecraft" / "config", destination )