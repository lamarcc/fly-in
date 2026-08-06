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

    def add_metadata(self, data: str, value: str):
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


class Parse():
    nb_drones = 0
    start_hub = (0, 0)
    end_hub = (0, 0)
    hubs = []
    hub_info = []
    connection = []

    param_state = {
        "nb_drones": 0,
        "start_hub": 0,
        "end_hub": 0,
    }

    @staticmethod
    def read_line(file: str):
        try:
            f = open(file)
            for line in f:
                if "#" in line:
                    continue
                if "\n" in line and len(line) == 1:
                    continue
                elif "nb_drones" in line:
                    if Parse.param_state["nb_drones"] == 0:
                        Parse.nb_drones = [int(n) for n in line.split() if n.isdigit()][0]
                        Parse.param_state["nb_drones"] = 1
                    else:
                        raise ValueError("Map file not conform, nb_drones doublon")
                elif "start_hub" in line.lower():
                    if Parse.param_state["start_hub"] == 0:
                        coord = [int(n) for n in line.split() if n.isdigit()]
                        if len(coord) != 2:
                            raise ValueError("Map file not conform, start_hub error")
                        Parse.start_hub = coord[0], coord[1]
                        Parse.hubs.append(line.strip('\n').split())
                        Parse.param_state["start_hub"] = 1
                    else:
                        raise ValueError("Map file not conform, start_hub doublon")
                elif "end_hub" in line.lower():
                    if Parse.param_state["end_hub"] == 0:
                        coord = [int(n) for n in line.split() if n.isdigit()]
                        if len(coord) != 2:
                            raise ValueError("Map file not conform, end_hub error")
                        Parse.end_hub = coord[0], coord[1]
                        Parse.hubs.append(line.strip('\n').split())
                        Parse.param_state["end_hub"] = 1
                    else:
                        raise ValueError("Map file not conform, end_hub doublon")
                elif Parse.parse_name(line.lower()) == "hub":
                    Parse.hubs.append(line.strip('\n').split())
                elif Parse.parse_name(line.lower()) == "connection":
                    Parse.connection.append(line.strip('\n').split())
                else:
                    raise ValueError("Error format")
        except FileNotFoundError:
            raise FileNotFoundError("File does not exist")
        except ValueError as e:
            print(e)

    @staticmethod
    def parse_name(line: str):
        name: str = ""
        for i in line.strip():
            if i == ":":
                return name.strip(" ")
            name += i
        return ""

    @staticmethod
    def is_valid_line(line: str):
        name = Parse.parse_name(line)
        if len(line.strip(name)):
            return True
        return False


Parse.read_line("../../maps/easy/01_linear_path.txt")
print(Parse.nb_drones)
print(Parse.start_hub)
print(Parse.end_hub)
print(Parse.hubs)
print(Parse.connection)
