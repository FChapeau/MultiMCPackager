from MultiMCPackager.mod import Mod
from pathlib import Path
import json


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

        self._loadModList(self.instance_path)

    def _loadModList(self, path:Path):
        self.mods = list()

        for file in path.glob(".minecraft/mods/*.jar"):
            self.mods.append(Mod(file))

    @property
    def name(self) -> str:
        return self.config["name"]
