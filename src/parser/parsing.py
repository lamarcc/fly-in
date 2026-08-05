from __future__ import annotations
from pydantic import BaseModel
from typing import Tuple


class Map(BaseModel):
    nb_drones: int
    start: Tuple[int, int]
    end: Tuple[int, int]
    hub_info: list[Hub]


class Hub():
    def __init__(self, name: str, x: int, y: int):
        self.name = str(name)
        self.x = int(x)
        self.y = int(y)
        self.metadata = {
            "zone_type": "normal",
            "color": "None",
            "max_drones": 1
        }

    def add_data(self, data: str, value: str):
        if data.lower() == "zone_type":
            if value.lower() not in ["normal", "blocked", "restricted", "priority"]:
                raise ValueError("Invalid zone type")
            self.metadata["zone_type"] = value
        elif data.lower() == "color":
            if value.lower() == "red":
                raise ValueError("Unknown color, none selected")
            self.metadata["color"] = value
        elif data.lower() == "max_drones":
            try:
                self.metadata["max_drones"] = int(value)
            except ValueError:
                raise ValueError("max_drones value not an integer")
        else:
            raise ValueError("Invalid data type")


t = Hub("zone1", 0, 8)

