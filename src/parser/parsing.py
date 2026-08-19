from __future__ import annotations
from typing import Tuple
import errors


class Color():
    list = [
        "none", "red", "green", "blue", "yellow",
        "orange", "purple", "pink", "brown",
        "black", "white", "gray", "cyan",
        "magenta", "lime", "navy", "teal",
    ]


class Parse():
    nb_drones = 0
    start_hub = {}
    end_hub = {}
    hubs = []
    known_position = []
    connection = []
    hub_name = []
    nb_line = 0
    err = []

    def parse(file: str):
        try:
            f = open(file)
            for line in f:
                try:
                    Parse.nb_line += 1
                    if line.startswith("#"):
                        continue
                    if line.startswith("\n") and len(line) == 1:
                        continue
                    key, info = line.split(":", 1)
                    key = key.strip().lower()
                    info = info.strip().lower()
                    Parse.check_line(key, info)
                    Parse.parse_key_info(key, info)
                except ValueError:
                    print(errors.MapFileError.msg(Parse.nb_line, "No key found (':' missing)"))
                except errors.MapFileError as e:
                    Parse.err.append(str(e))
            if Parse.err:
                for error in Parse.err:
                    print(error)
        except FileNotFoundError:
            print(errors.MapFileError.msg(Parse.nb_line, "File does not exist"))

    @staticmethod
    def check_line(key, info):
        m_start = info.find("[")
        m_end = info.find("]")
        if m_start != -1 and m_end != -1:
            tmp = info.replace(info[m_start:m_end + 1], "")
            if (key == "hub" and len(tmp.split()) > 3) or (key == "connection" and len(tmp.split()) > 1):
                Parse.err.append(errors.InvalidLineError(Parse.nb_line))
        else:
            if (key == "hub" and len(info.split()) > 3) or (key == "connection" and len(info.split()) > 1):
                Parse.err.append(errors.InvalidLineError(Parse.nb_line))

    @staticmethod
    def parse_key_info(key: str, info: str):
        if key == "nb_drones":
            try:
                if Parse.nb_drones == 0:
                    if int(info) < 1:
                        raise errors.InvalidDronesValue(Parse.nb_line, "Cant have less than 1 drone")
                    Parse.nb_drones = int(info)
                else:
                    raise errors.DoublonError(Parse.nb_line, key)
            except ValueError:
                raise errors.InvalidDronesValue(Parse.nb_line, "'nb_drones' value need to be an integer")
        elif key == "start_hub":
            if not Parse.start_hub:
                Parse.start_hub = Parse.parse_hub(info)
                Parse.try_position(Parse.start_hub)
                Parse.hubs.append(Parse.start_hub)
            else:
                raise errors.HubError(Parse.nb_line, "Can't have 2 start_hub")
        elif key == "end_hub":
            if not Parse.end_hub:
                Parse.end_hub = Parse.parse_hub(info)
                Parse.try_position(Parse.end_hub)
                Parse.hubs.append(Parse.end_hub)
            else:
                raise errors.HubError(Parse.nb_line, "Can't have 2 end_hub")
        elif key == "hub":
            tmp_hub = Parse.parse_hub(info)
            Parse.try_position(tmp_hub)
            Parse.hubs.append(tmp_hub)
        elif key == "connection":
            parsed_connection = Parse.parse_connection(info)
            for connection in Parse.connection:
                if set(parsed_connection["connection"]) == set(connection["connection"]):
                    Parse.err.append(errors.DoublonError(Parse.nb_line, parsed_connection["connection"]))
            hub1, hub2 = parsed_connection["connection"]
            if hub1 not in Parse.hub_name and hub1 is not None:
                Parse.err.append(errors.HubError(Parse.nb_line, f"Hub '{hub1}' not defined yet"))
            if hub2 not in Parse.hub_name and hub2 is not None:
                Parse.err.append(errors.HubError(Parse.nb_line, f"Hub '{hub2}' not defined yet"))
            Parse.connection.append(parsed_connection)
        else:
            raise errors.InvalidKeyError(Parse.nb_line, key)

    @staticmethod
    def try_position(hub_info):
        try:
            x = int(hub_info["pos_x"])
            y = int(hub_info["pos_y"])
            for verif in Parse.hubs:
                if x == verif["pos_x"] and y == verif["pos_y"]:
                    Parse.err.append(errors.HubError(Parse.nb_line, f"Position <{x}, {y}> already occupied by Hub: {verif['name']}"))
            hub_info["pos_x"] = int(hub_info["pos_x"])
            hub_info["pos_y"] = int(hub_info["pos_y"])
        except ValueError:
            raise errors.HubError(Parse.nb_line, f"Undefined '{hub_info['name']}' hub position")

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
            if hub_info["name"] in Parse.hub_name:
                Parse.err.append(errors.HubError(Parse.nb_line, f"'{hub_info['name']}' already defined earlier"))
            Parse.hub_name.append(hub_info["name"])
            hub_info["metadata"] = Parse.parse_metadata(hub_info["name"], line[metadata_index:], default_metadata)
            return {**default_info, **hub_info}
        else:
            tmp_line = line.strip()
            hub_info = {key: value for key, value in zip(["name", "pos_x", "pos_y"], tmp_line.split())}
            if hub_info["name"] in Parse.hub_name:
                Parse.err.append(errors.HubError(Parse.nb_line, f"'{hub_info['name']}' already defined earlier"))
            Parse.hub_name.append(hub_info["name"])
            hub_info["metadata"] = default_metadata
            return {**default_info, **hub_info}

    @staticmethod
    def parse_metadata(name, info, default_metadata):
        info = [i.split("=") for i in info.strip("[]").split()]
        for verif_format in info:
            if len(verif_format) == 1:
                verif_format.append("undefined")
            elif len(verif_format) == 2 and verif_format[1] == "":
                if verif_format[0] == "zone":
                    print(errors.MapFileError.warning(Parse.nb_line, f"Value is missing for '{verif_format[0]}', 'normal' set by default"))
                    verif_format[1] = "normal"
                elif verif_format[0] == "max_drones":
                    print(errors.MapFileError.warning(Parse.nb_line, f"Value is missing for '{verif_format[0]}', '1' set by default"))
                    verif_format[1] = 1
            elif len(verif_format) > 2:
                info.remove(verif_format)
                Parse.err.append(errors.MetadataError(Parse.nb_line, "Typing incorrect, follow <metadata=info>"))
        new_metadata = {**default_metadata, **{key: value for key, value in info}}
        try:
            for key in new_metadata.keys():
                if key not in ["zone", "color", "max_drones"]:
                    Parse.err.append(errors.MetadataError(Parse.nb_line, f"Unknown metadata '{key}'"))
            if "zone" in new_metadata and new_metadata["zone"] not in ["normal", "blocked", "restricted", "priority"]:
                Parse.err.append(errors.HubError(Parse.nb_line, f"Invalid zone_type '{new_metadata['zone']}'"))
            if "color" in new_metadata and new_metadata["color"].lower() not in Color.list:
                print(errors.MapFileError.warning(Parse.nb_line, f"Unknown color for hub '{name}', color set to grey by default"))
                new_metadata["color"] = "grey"
            if "max_drones" in new_metadata:
                new_metadata["max_drones"] = int(new_metadata["max_drones"])
        except ValueError:
            Parse.err.append(errors.InvalidDronesValue(Parse.nb_line, "Invalid 'max_drones' value"))
        return new_metadata

    @staticmethod
    def parse_connection(line: str):
        default_metadata = {"max_link_capacity": 1}
        metadata_index = line.find("[")
        invalid_data = []
        if metadata_index != -1:
            link = line[:metadata_index].strip().split("-")
            if len(link) != 2:
                Parse.err.append(errors.ConnectionError(Parse.nb_line, "Connection invalid, follow <from-to>"))
                link = [None, None]
            info = [i.split("=") for i in line[metadata_index:].strip("[]").split()]
            for verif_format in info:
                if len(verif_format) == 1:
                    Parse.err.append(errors.MetadataError(Parse.nb_line, "Missing value after metadata key, follow <metadata=value>"))
                    verif_format.append("undefined")
                elif len(verif_format) == 2 and verif_format[1] == "":
                    print(errors.MapFileError.warning(Parse.nb_line, f"Value is missing for '{verif_format[0]}', '1' set by default"))
                    verif_format[1] = 1
                elif len(verif_format) > 2:
                    info.remove(verif_format)
                    Parse.err.append(errors.MetadataError(Parse.nb_line, "Typing incorrect, follow <metadata=info>"))
            metadata = {key: value for key, value in info}
            try:
                for check_metadata in metadata.keys():
                    if check_metadata != "max_link_capacity":
                        invalid_data.append(check_metadata)
                if len(invalid_data):
                    Parse.err.append(errors.MetadataError(Parse.nb_line, f"Unknown metadata '{invalid_data}'"))
                metadata["max_link_capacity"] = int(metadata["max_link_capacity"])
            except ValueError:
                Parse.err.append(errors.ConnectionError(Parse.nb_line, "Value need to be an integer for 'max_link_capacity'"))
            return {"connection": link, "metadata": metadata}
        else:
            link = line.strip().split("-")
            if len(link) != 2:
                Parse.err.append(errors.ConnectionError(Parse.nb_line, "Connection invalid, follow <from-to>"))
                link = [None, None]
            return {"connection": link, "metadata": default_metadata}


Parse.parse("../../maps/easy/01_linear_path.txt")
print(Parse.nb_drones)
print(Parse.start_hub)
print(Parse.end_hub)
for hub in Parse.hubs:
    print(hub)
for connection in Parse.connection:
    print(connection)
