from pick import pick
from pathlib import Path
from parser.errors import Colors
from typing import Any


class EmptyMapFolder(Exception):
    def __init__(self) -> None:
        self.template = (
                f'{Colors.FAIL}'
                f'{Colors.BOLD}'
                f'[EmptyMapFolder] '
                f'{Colors.ENDC}'
        )

    def __str__(self) -> Any:
        return self.template + "Map Folder is empty"


class MapMenu():
    def __init__(self) -> None:
        self.maps_dir = Path("maps")

    def choose(self) -> Path:
        try:
            while True:
                dir = [
                    self.get_name(path)
                    for path in self.maps_dir.iterdir()
                    if path.is_dir() or path.suffix.lower() == ".txt"
                ]
                path, b = pick(dir, "Choose your map")
                self.maps_dir /= path
                if self.maps_dir.is_file():
                    return self.maps_dir
        except ValueError:
            raise EmptyMapFolder()

    def get_name(self, path: Path) -> str:
        return path.parts[len(path.parts) - 1]
