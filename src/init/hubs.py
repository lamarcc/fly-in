from __future__ import annotations
from pydantic import BaseModel
from typing import Tuple
from .parser import Parse

class Map(BaseModel):
    nb_drones: int
    start: Tuple[int, int]
    end: Tuple[int, int]
    hub_info: list[Hub]


class Hub():
    def __init__(self, name: str, x: int, y: int):
        try:
            self.name = str(name)
            self.x = int(x)
            self.y = int(y)
            self.metadata = {
                "zone_type": "normal",
                "color": "None",
                "max_drones": 1
            }
            self.connection: list[Tuple[Tuple[int, int]]] = []
        except ValueError:
            raise ValueError("Invalid hub informations")

    def add_metadata(self, data: dict):
        if data["zone_type"].lower() not in ["normal", "blocked", "restricted", "priority"]:
            raise ValueError("Invalid zone type")
        self.metadata["zone_type"] = data["zone_type"]
        elif data.lower() == "color":
            self.metadata["color"] = value
        elif data.lower() == "max_drones":
            try:
                self.metadata["max_drones"] = int(value)
            except ValueError:
                raise ValueError("max_drones value not an integer")
        else:
            raise ValueError("Invalid data type")


