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
                hub_name = [name["name"] for name, _ in Parse.hubs]
                if line.startswith("#"):
                    continue
                if line.startswith("\n") and len(line) == 1:
                    continue
                key, info = line.split(":", 1)
                key = key.strip()
                info = info.strip()
                if key == "nb_drones":
                    if Parse.param_state["nb_drones"] == 0:
                        try:
                            Parse.nb_drones = int(info)
                            Parse.param_state["nb_drones"] = 1
                        except ValueError:
                            raise ValueError("Error nb_drones value")
                    else:
                        raise ValueError("Map file not conform, nb_drones doublon")
                elif key == "start_hub":
                    if Parse.param_state["start_hub"] == 0:
                        try:
                            Parse.start_hub = Parse.parse_hub(info)
                            Parse.try_position(Parse.start_hub)
                            Parse.param_state["start_hub"] = 1
                            Parse.hubs.append(Parse.start_hub)
                        except ValueError as e:
                            raise ValueError(f"Error '{Parse.start_hub[0]['name']}': {e}")
                    else:
                        raise ValueError("Map file not conform, start_hub doublon")
                elif key == "end_hub":
                    if Parse.param_state["end_hub"] == 0:
                        try:
                            Parse.end_hub = Parse.parse_hub(info)
                            Parse.try_position(Parse.end_hub)
                            Parse.param_state["end_hub"] = 1
                            Parse.hubs.append(Parse.end_hub)
                        except ValueError as e:
                            raise ValueError(f"Error '{Parse.end_hub[0]['name']}': {e}")
                    else:
                        raise ValueError("Map file not conform, end_hub doublon")
                elif key == "hub":
                    try:
                        tmp = Parse.parse_hub(info)
                        Parse.try_position(tmp)
                        if tmp[0]["name"] in hub_name:
                            raise ValueError("already exist")
                    except ValueError as e:
                        raise ValueError(f"Error '{tmp[0]['name']}': {e}")
                    Parse.hubs.append(tmp)
                elif key == "connection":
                    try:
                        info = info.split("-")
                        for connection in Parse.connection:
                            if set(info) == set(connection):
                                raise ValueError("connection already exist")
                        hub1, hub2 = info
                        if hub1 not in hub_name:
                            raise ValueError("Hub not defined yet!")
                        if hub2 not in hub_name:
                            raise ValueError("Hub not defined yet!")
                        Parse.connection.append(info)
                    except ValueError as e:
                        raise ValueError(f"Error '{info}': {e}")
                else:
                    raise ValueError("Error format")
        except FileNotFoundError:
            raise FileNotFoundError("File does not exist")
        except ValueError as e:
            print(e)

    @staticmethod
    def parse_hub(line: str):
        default_info = {"name": "undefined", "pos_x": "undefined", "pos_y": "undefined"}
        default_metadata = {"zone": "normal", "max_drones": "1", "color": "none"}
        hub_info = {}
        tmp_line = ""
        metadata_index = line.find("[")
        if metadata_index != -1:
            tmp_line = line[:metadata_index].strip()
            hub_info = {key: value for key, value in zip(["name", "pos_x", "pos_y"], tmp_line.split())}
            metadata = Parse.parse_metadata(line[metadata_index:], default_metadata)
            return {**default_info, **hub_info}, metadata
        tmp_line = line.strip()
        hub_info = {key: value for key, value in zip(["name", "pos_x", "pos_y"], tmp_line.split())}
        return {**default_info, **hub_info}, default_metadata

    @staticmethod
    def parse_metadata(line, default_metadata):
        line = [i.split("=") for i in line.strip("[]").split()]
        new_metadata = {key: value for key, value in line}
        return {**default_metadata, **new_metadata}

    @staticmethod
    def try_position(hub_info):
        try:
            int(hub_info[0]["pos_x"])
            int(hub_info[0]["pos_y"])
        except ValueError:
            raise ValueError("undefined position")

try:
    Parse.read_line("../maps/easy/01_linear_path.txt")
except ValueError:
    print("coucou")
print(Parse.nb_drones)
print(Parse.hubs)
print(Parse.connection)
