from __future__ import annotations
from typing import Tuple
from . import errors


class Color():
    list = [
        "none", "red", "green", "blue", "yellow",
        "orange", "purple", "pink", "brown",
        "black", "white", "gray", "cyan",
        "magenta", "lime", "navy", "teal",
    ]


class Parse():
    def __init__(self):
        self.nb_drones = 0
        self.start_hub = {}
        self.end_hub = {}
        self.hubs = []
        self.known_position = []
        self.connection = []
        self.hub_name = []
        self.nb_line = 0
        self.err = []

    def parse(self, file: str):
        try:
            f = open(file)
            for line in f:
                try:
                    self.nb_line += 1
                    if line.startswith("#"):
                        continue
                    if line.startswith("\n") and len(line) == 1:
                        continue
                    key, info = line.split(":", 1)
                    key = key.strip().lower()
                    info = info.strip().lower()
                    self.check_line(key, info)
                    self.parse_key_info(key, info)
                except ValueError:
                    print(errors.MapFileError.msg(self.nb_line, "No key found (':' missing)"))
                except errors.MapFileError as e:
                    self.err.append(str(e))
            if self.err:
                for error in self.err:
                    print(error)
                raise errors.ParsingError
        except FileNotFoundError:
            print(errors.MapFileError.msg(self.nb_line, "File does not exist"))

    def check_line(self, key, info):
        m_start = info.find("[")
        m_end = info.find("]")
        if m_start != -1 and m_end != -1:
            tmp = info.replace(info[m_start:m_end + 1], "")
            if (key == "hub" and len(tmp.split()) > 3) or (key == "connection" and len(tmp.split()) > 1):
                self.err.append(errors.InvalidLineError(self.nb_line))
        else:
            if (key == "hub" and len(info.split()) > 3) or (key == "connection" and len(info.split()) > 1):
                self.err.append(errors.InvalidLineError(self.nb_line))

    def parse_key_info(self, key: str, info: str):
        if key == "nb_drones":
            try:
                if self.nb_drones == 0:
                    if int(info) < 1:
                        raise errors.InvalidValue(self.nb_line, "Cant have less than 1 drone")
                    self.nb_drones = int(info)
                else:
                    raise errors.DoublonError(self.nb_line, key)
            except ValueError:
                raise errors.InvalidValue(self.nb_line, "'nb_drones' value need to be an integer")
        elif key == "start_hub":
            if not self.start_hub:
                self.start_hub = self.parse_hub(info)
                self.try_position(self.start_hub)
                self.hubs.append(self.start_hub)
            else:
                raise errors.HubError(self.nb_line, "Can't have 2 start_hub")
        elif key == "end_hub":
            if not self.end_hub:
                self.end_hub = self.parse_hub(info)
                self.try_position(self.end_hub)
                self.hubs.append(self.end_hub)
            else:
                raise errors.HubError(self.nb_line, "Can't have 2 end_hub")
        elif key == "hub":
            tmp_hub = self.parse_hub(info)
            self.try_position(tmp_hub)
            self.hubs.append(tmp_hub)
        elif key == "connection":
            parsed_connection = self.parse_connection(info)
            hub1, hub2 = parsed_connection["hub_a"], parsed_connection["hub_b"]
            for connection in self.connection:
                if set([hub1, hub2]) == set([connection["hub_a"], connection["hub_b"]]):
                    self.err.append(errors.ConnectionError(self.nb_line, f"Connection already defined earlier <{parsed_connection['hub_a']}-{parsed_connection['hub_b']}>"))
            if hub1 not in self.hub_name and hub1 is not None:
                raise errors.HubError(self.nb_line, f"Hub '{hub1}' not defined yet")
            if hub2 not in self.hub_name and hub2 is not None:
                raise errors.HubError(self.nb_line, f"Hub '{hub2}' not defined yet")
            self.connection.append(parsed_connection)
        else:
            raise errors.InvalidKeyError(self.nb_line, key)

    def try_position(self, hub_info):
        try:
            x = int(hub_info["pos_x"])
            y = int(hub_info["pos_y"])
            for verif in self.hubs:
                if x == verif["pos_x"] and y == verif["pos_y"]:
                    self.err.append(errors.HubError(self.nb_line, f"Position <{x}, {y}> already occupied by Hub: {verif['name']}"))
            hub_info["pos_x"] = int(hub_info["pos_x"])
            hub_info["pos_y"] = int(hub_info["pos_y"])
            if hub_info["pos_x"] < 0 or hub_info["pos_y"] < 0:
                self.err.append(errors.InvalidValue(self.nb_line, "Invalid coordinates, minimum is 0"))
        except ValueError:
            raise errors.HubError(self.nb_line, f"Undefined '{hub_info['name']}' hub position")

    def parse_hub(self, line: str):
        default_info = {"name": "undefined", "pos_x": "undefined", "pos_y": "undefined"}
        default_metadata = {"zone": "normal", "max_drones": "1", "color": "none"}
        hub_info = {}
        tmp_line = ""
        metadata_index = line.find("[")
        if metadata_index != -1:
            tmp_line = line[:metadata_index].strip()
            hub_info = {key: value for key, value in zip(["name", "pos_x", "pos_y"], tmp_line.split())}
            if hub_info["name"] in self.hub_name:
                self.err.append(errors.HubError(self.nb_line, f"'{hub_info['name']}' already defined earlier"))
            self.hub_name.append(hub_info["name"])
            hub_info["metadata"] = self.parse_metadata(hub_info["name"], line[metadata_index:], default_metadata)
            return {**default_info, **hub_info}
        else:
            tmp_line = line.strip()
            hub_info = {key: value for key, value in zip(["name", "pos_x", "pos_y"], tmp_line.split())}
            if hub_info["name"] in self.hub_name:
                self.err.append(errors.HubError(self.nb_line, f"'{hub_info['name']}' already defined earlier"))
            self.hub_name.append(hub_info["name"])
            hub_info["metadata"] = default_metadata
            return {**default_info, **hub_info}

    def parse_metadata(self, name, info, default_metadata):
        info = [i.split("=") for i in info.strip("[]").split()]
        for verif_format in info:
            if len(verif_format) == 1:
                verif_format.append("undefined")
            elif len(verif_format) == 2 and verif_format[1] == "":
                if verif_format[0] == "zone":
                    print(errors.MapFileError.warning(self.nb_line, f"Value is missing for '{verif_format[0]}', 'normal' set by default"))
                    verif_format[1] = "normal"
                elif verif_format[0] == "max_drones":
                    print(errors.MapFileError.warning(self.nb_line, f"Value is missing for '{verif_format[0]}', '1' set by default"))
                    verif_format[1] = 1
            elif len(verif_format) > 2:
                info.remove(verif_format)
                self.err.append(errors.MetadataError(self.nb_line, "Typing incorrect, follow <metadata=info>"))
        new_metadata = {**default_metadata, **{key: value for key, value in info}}
        try:
            for key in new_metadata.keys():
                if key not in ["zone", "color", "max_drones"]:
                    self.err.append(errors.MetadataError(self.nb_line, f"Unknown metadata '{key}'"))
            if "zone" in new_metadata and new_metadata["zone"] not in ["normal", "blocked", "restricted", "priority"]:
                self.err.append(errors.HubError(self.nb_line, f"Invalid zone_type '{new_metadata['zone']}'"))
            if "color" in new_metadata and new_metadata["color"] not in Color.list:
                print(errors.MapFileError.warning(self.nb_line, f"Unknown color for hub '{name}', color set to grey by default"))
                new_metadata["color"] = "grey"
            if "max_drones" in new_metadata:
                new_metadata["max_drones"] = int(new_metadata["max_drones"])
                if new_metadata["max_drones"] < 1:
                    self.err.append(errors.InvalidValue(self.nb_line, "Invalid 'max_drones' value, minimum is 1"))
        except ValueError:
            self.err.append(errors.InvalidValue(self.nb_line, "Invalid 'max_drones' value"))
        return new_metadata

    def parse_connection(self, line: str):
        default_metadata = {"max_link_capacity": 1}
        metadata_index = line.find("[")
        invalid_data = []
        if metadata_index != -1:
            link = line[:metadata_index].strip().split("-")
            if len(link) != 2:
                self.err.append(errors.ConnectionError(self.nb_line, "Connection invalid, follow <from-to>"))
                link = [None, None]
            info = [i.split("=") for i in line[metadata_index:].strip("[]").split()]
            for verif_format in info:
                if len(verif_format) == 1:
                    self.err.append(errors.MetadataError(self.nb_line, "Missing value after metadata key, follow <metadata=value>"))
                    verif_format.append("undefined")
                elif len(verif_format) == 2 and verif_format[1] == "":
                    print(errors.MapFileError.warning(self.nb_line, f"Value is missing for '{verif_format[0]}', '1' set by default"))
                    verif_format[1] = 1
                elif len(verif_format) > 2:
                    info.remove(verif_format)
                    self.err.append(errors.MetadataError(self.nb_line, "Typing incorrect, follow <metadata=info>"))
            metadata = {key: value for key, value in info}
            try:
                for check_metadata in metadata.keys():
                    if check_metadata != "max_link_capacity":
                        invalid_data.append(check_metadata)
                if len(invalid_data):
                    self.err.append(errors.MetadataError(self.nb_line, f"Unknown metadata '{invalid_data}'"))
                metadata["max_link_capacity"] = int(metadata["max_link_capacity"])
                if metadata["max_link_capacity"] < 1:
                    self.err.append(errors.InvalidValue(self.nb_line, "Invalid 'max_link_capacity' value, minimum is 1"))
            except ValueError:
                self.err.append(errors.ConnectionError(self.nb_line, "Value need to be an integer for 'max_link_capacity'"))
            return {"hub_a": link[0], "hub_b": link[1], "metadata": metadata}
        else:
            link = line.strip().split("-")
            if len(link) != 2:
                self.err.append(errors.ConnectionError(self.nb_line, "Connection invalid, follow <from-to>"))
                link = [None, None]
            return {"hub_a": link[0], "hub_b": link[1], "metadata": default_metadata}
