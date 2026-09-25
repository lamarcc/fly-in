from pick import pick
from pathlib import Path
from parser.errors import Colors
from typing import Any


class EmptyMapFolder(Exception):
    """Exception raised when the map folder is empty."""

    def __init__(self) -> None:
        """Initialize the exception with a formatted message."""
        self.template = (
                f'{Colors.FAIL}'
                f'{Colors.BOLD}'
                f'[EmptyMapFolder] '
                f'{Colors.ENDC}'
        )

    def __str__(self) -> Any:
        """Return the formatted exception message."""
        return self.template + "Map Folder is empty"


class MapMenu():
    """Manager for interactive selection of map files.

    Allows the user to browse the map directory and select a specific map file.
    """

    def __init__(self) -> None:
        """Initialize the menu with the map directory path."""
        self.maps_dir = Path("maps")

    def choose(self) -> Path:
        """Display an interactive menu to select a map.

        Lets the user navigate through directories or directly
         select a map file (.txt).

        Returns:
            Path: The absolute path of the selected map file.

        Raises:
            EmptyMapFolder: If the maps folder is empty.
        """
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
        """Extract the file or folder name from a path.

        Args:
            path: The path to extract the name from.

        Returns:
            str: The name of the last element in the path.
        """
        return path.parts[len(path.parts) - 1]
