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
    start_hub = {}
    end_hub = {}
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
                elif line.split(": ")[0] == "nb_drones":
                    if Parse.param_state["nb_drones"] == 0:
                        line = line.split()
                        if len(line) != 2:
                            raise ValueError("Error nb_drones line")
                        try:
                            Parse.nb_drones = int(line[1])
                            Parse.param_state["nb_drones"] = 1
                        except ValueError:
                            raise ValueError("Error nb_drones value")
                    else:
                        raise ValueError("Map file not conform, nb_drones doublon")
                elif line.split(": ")[0] == "start_hub":
                    if Parse.param_state["start_hub"] == 0:
                        Parse.start_hub = Parse.parse_hub(line.lower())
                        Parse.param_state["start_hub"] = 1
                    else:
                        raise ValueError("Map file not conform, start_hub doublon")
                elif line.split(": ")[0] == "end_hub":
                    if Parse.param_state["end_hub"] == 0:
                        Parse.end_hub = Parse.parse_hub(line.lower())
                        Parse.param_state["end_hub"] = 1
                    else:
                        raise ValueError("Map file not conform, end_hub doublon")
                elif line.split(": ")[0] == "hub":
                    Parse.hubs.append(Parse.parse_hub(line.strip('\n')))
                elif line.split(": ")[0] == "connection":
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
    def parse_hub(line: str):
        default_info = {"name": "undefined", "pos_x": "undefined", "pos_y": "undefined"}
        default_metadata = {"zone": "normal", "max_drones": "1", "color": "grey"}
        hub_info = {}
        tmp_line = ""
        cpy_state = 0
        i = 0
        for c in line:
            if c == ":":
                cpy_state = 1
                continue
            if c == "[":
                hub_info = {key: value for key, value in zip(["name", "pos_x", "pos_y"], tmp_line.split())}
                metadata = Parse.parse_metadata(line[i:].strip(), default_metadata)
                return {**default_info, **hub_info}, metadata
            if cpy_state == 1:
                tmp_line += c
            i += 1
        hub_info = {key: value for key, value in zip(["name", "pos_x", "pos_y"], tmp_line.split())}
        return {**default_info, **hub_info}, default_metadata

    @staticmethod
    def parse_metadata(line, default_metadata):
        line = [i.split("=") for i in line.strip("[]").split()]
        new_metadata = {key: value for key, value in line}
        return {**default_metadata, **new_metadata}

    @staticmethod
    def parse_connection(line):


Parse.read_line("../maps/easy/01_linear_path.txt")
print(Parse.nb_drones)
print(Parse.start_hub)
print(Parse.end_hub)
print(Parse.hubs)
print(Parse.connection)
# print(Parse.parse_hub("hub: roof13 4"))
# print(Parse.parse_hub("hub: roof2 6 2 [zone=normal]"))
# print(Parse.parse_hub("hub: obstacleX -5 -5 [zone=blocked]"))
# print(Parse.parse_hub("hub: corridorA 4 3 [zone=priority color=green max_drones=2]"))
