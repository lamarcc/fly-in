from __future__ import annotations
from pydantic import BaseModel
from typing import Tuple


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
    def parse_line(file: str):
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
                Parse.check_line(info)
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
                        print(Parse.parse_connection(info))
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
    def parse_connection(line: str):
        default_metadata = {"max_link_capacity": 1}
        metadata_index = line.find("[")
        invalid_data = []
        if metadata_index != -1:
            metadata = dict([i.split("=") for i in line[metadata_index:].strip("[]").split()])
            for check_metadata in metadata.keys():
                if check_metadata != "max_link_capacity":
                    invalid_data.append(check_metadata)
            if len(invalid_data):
                raise ValueError(f"invalid metadata '{invalid_data}'")
            return {"info": line[:metadata_index].strip().split("-"), "metadata": metadata}
        else:
            return {"info": line.strip().split("-"), "metadata": default_metadata}


    @staticmethod
    def parse_metadata(line, default_metadata):
        line = [i.split("=") for i in line.strip("[]").split()]
        new_metadata = {key: value for key, value in line}
        # try:
        #     if new_metadata["zone_type"] not in ["normal", "blocked", "restricted", "priority"]:
        #         raise ValueError("invalid zone_type")
        #     if new_metadata["color"] not in:
        #         raise ValueError("invalid zone_type")
        return {**default_metadata, **new_metadata}

    @staticmethod
    def try_position(hub_info):
        try:
            int(hub_info[0]["pos_x"])
            int(hub_info[0]["pos_y"])
        except ValueError:
            raise ValueError("undefined position")

    @staticmethod
    def check_line(line):
        m_start = line.find("[")
        m_end = line.find("]")
        print(line)
        if m_start != -1 and m_end != -1:
            tmp = line.replace(line[m_start:m_end + 1], "")
            if len(tmp.split()) > 3:
                raise ValueError("too much arguments")
            return tmp
        else:
            if len(line.split()) > 3:
                raise ValueError("too much arguments")    


Parse.parse_line("../../maps/easy/01_linear_path.txt")
print(Parse.hubs)
