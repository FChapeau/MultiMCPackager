from pathlib import Path
from zipfile import ZipFile
import json


class Mod(object):
    def __init__(self, path: Path):
        self.filename = path.name
        self.modpath = path
        self.clientonly = "clientonly" in path.name
        self.serveronly = "serveronly" in path.name
        self.mods = list()

        with ZipFile(path) as modjar:
            if "mcmod.info" in modjar.namelist():
                with modjar.open("mcmod.info", 'r') as metafile:
                    filecontents = metafile.read().decode("utf-8").replace("\n", "")
                    metadata = json.loads(filecontents)

                    if "modList" in metadata:
                        metadata = metadata.get("modList")

                    for child in metadata:
                        self.mods.append(ModMetadata(child))


class ModMetadata(object):
    def __init__(self, info: dict):
        self.name = info.get("name")
        self.modid = info.get("modid")
        self.version = info.get("version")
