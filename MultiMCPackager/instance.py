from MultiMCPackager.mod import Mod
from pathlib import Path


class Instance(object):
    def __init__(self, path):
        instancepath = Path(path)

        with open(instancepath/"instance.cfg") as f:
            lines = f.readlines()
            self.config = dict()
            for line in lines:
                key, value = line.split("=")
                self.config[key] = value

    @property
    def name(self) -> str:
        return self.config["name"]
