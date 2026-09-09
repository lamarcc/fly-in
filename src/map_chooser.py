from pick import pick
from pathlib import Path


class MapMenu():
    def __init__(self) -> None:
        self.maps_dir = Path("maps")

    def choose(self) -> Path:
        while True:
            dir = [self.get_name(path) for path in self.maps_dir.iterdir() if path.is_dir() or path.suffix.lower() == ".txt"]
            path, b = pick(dir, "Choose your map")
            self.maps_dir /= path
            if self.maps_dir.is_file():
                return self.maps_dir

    def get_name(self, path: Path) -> str:
        return path.parts[len(path.parts) - 1]
