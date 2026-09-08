from pick import pick
from pathlib import Path

class MapMenu():
    def __init__(self):
        self.maps_dir = Path("../maps")

    def choose(self):
        choose = [path for path in self.maps_dir.iterdir() if path.is_dir()]
        path, b = pick(choose, "Choose your map")
        p = self.dir_name(path)
        print(p)

    def dir_name(self, path):
        if path.is_dir():
            return path.parts[1:]

