from __future__ import annotations
from pydantic import BaseModel
from typing import Tuple


class Parse():
    nb_drones = 0
    start_hub = {}
    end_hub = {}
    hubs = []
    connection = []
    hub_name = []
    nb_line = 0

    @staticmethod
    def parse(file: str):
        try:
            f = open(file)
            for line in f:
                Parse.nb_line += 1
                if line.startswith("#"):
                    continue
                if line.startswith("\n") and len(line) == 1:
                    continue
                key, info = line.split(":", 1)
                key = key.strip()
                info = info.strip()
                Parse.check_line(key, info)
                Parse.parse_key_info(key, info)
        except FileNotFoundError:
            raise FileNotFoundError("File does not exist")
        except ValueError as e:
            print(e)

    @staticmethod
    def parse_key_info(key: str, info: str):
        if key == "nb_drones":
            try:
                if Parse.nb_drones == 0:
                    if int(info) < 1:
                        raise ValueError("invalid value")
                    Parse.nb_drones = int(info)
                else:
                    raise ValueError("already defined earlier")
            except ValueError as e:
                raise ValueError(f"[Error] line {Parse.nb_line}: {e}")
        elif key == "start_hub":
            try:
                if not Parse.start_hub:
                    Parse.start_hub = Parse.parse_hub(info)
                    Parse.try_position(Parse.start_hub)
                    Parse.hubs.append(Parse.start_hub)
                    Parse.hub_name.append(Parse.start_hub["name"])
                else:
                    raise ValueError("'start_hub' already defined earlier")
            except ValueError as e:
                raise ValueError(f"[Error] line {Parse.nb_line}: {e}")
        elif key == "end_hub":
            try:
                if not Parse.end_hub:
                    Parse.end_hub = Parse.parse_hub(info)
                    Parse.try_position(Parse.end_hub)
                    Parse.hubs.append(Parse.end_hub)
                    Parse.hub_name.append(Parse.end_hub["name"])
                else:
                    raise ValueError("'end_hub' already defined earlier")
            except ValueError as e:
                raise ValueError(f"[Error] line {Parse.nb_line}: {e}")
        elif key == "hub":
            try:
                tmp_hub = Parse.parse_hub(info)
                Parse.try_position(tmp_hub)
                if tmp_hub["name"] in Parse.hub_name:
                    raise ValueError("already exist")
                Parse.hubs.append(tmp_hub)
                Parse.hub_name.append(tmp_hub["name"])
            except ValueError as e:
                raise ValueError(f"[Error] line {Parse.nb_line}: {e}")
        elif key == "connection":
            try:
                if info.find("[") != -1 and info.find("]") != -1:
                    info = info.replace(info[info.find("["):info.find("]")+1], "")
                info = info.strip().split("-")
                for connection in Parse.connection:
                    if set(info) == set(connection):
                        raise ValueError(f"'{connection}' already defined earlier")
                hub1, hub2 = info
                if hub1 not in Parse.hub_name:
                    raise ValueError(f"'{hub1}' not defined yet")
                if hub2 not in Parse.hub_name:
                    raise ValueError(f"'{hub2}' not defined yet")
                Parse.connection.append(info)
            except ValueError as e:
                raise ValueError(f"[Error] line {Parse.nb_line}: {e}")
        else:
            raise ValueError(f"[Error] line {Parse.nb_line}: invalid key")

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
            hub_info["metadata"] = metadata
            return {**default_info, **hub_info}
        tmp_line = line.strip()
        hub_info = {key: value for key, value in zip(["name", "pos_x", "pos_y"], tmp_line.split())}
        hub_info["metadata"] = default_metadata
        return {**default_info, **hub_info}

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
            return {"connection": line[:metadata_index].strip().split("-"), "metadata": metadata}
        else:
            return {"connection": line.strip().split("-"), "metadata": default_metadata}

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
            int(hub_info["pos_x"])
            int(hub_info["pos_y"])
        except ValueError:
            raise ValueError("undefined position")

    @staticmethod
    def check_line(key, info):
        m_start = info.find("[")
        m_end = info.find("]")
        if m_start != -1 and m_end != -1:
            tmp = info.replace(info[m_start:m_end + 1], "")
            if (key == "hub" and len(tmp.split()) > 3) or (key == "connection" and len(tmp.split()) > 1):
                raise ValueError("too much arguments")
            return tmp
        else:
            if (key == "hub" and len(tmp.split()) > 3) or (key == "connection" and len(tmp.split()) > 1):
                raise ValueError("too much arguments")


Parse.parse("../../maps/easy/01_linear_path.txt")
print(Parse.hubs)
# print(Parse.connection)
