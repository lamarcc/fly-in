from __future__ import annotations
from typing import Any
from . import errors
import sys


class Color():
    list = [
        "none", "red", "green", "blue", "yellow",
        "orange", "purple", "pink", "brown",
        "black", "white", "gray", "cyan",
        "magenta", "lime", "navy", "teal",
        "maroon", "gold", "darkred", "violet",
        "crimson", "rainbow"
    ]


class Parse():
    def __init__(self) -> None:
        self.nb_drones: Any = None
        self.nb_drones_check: int = 0
        self.start_hub: dict = {}
        self.end_hub: dict = {}
        self.hubs: list = []
        self.known_position: list = []
        self.connection: list = []
        self.hub_name: list[str] = []
        self.nb_line: int = 0
        self.err: list = []

    def parse(self, file: str) -> None:
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
                    if self.nb_drones_check == 0:
                        self.err.append(errors.MapFileError.msg(
                            "<nb_drones> must be the first line to be defined",
                            self.nb_line)
                        )
                        self.nb_drones_check = 1
                except ValueError:
                    print(errors.MapFileError.msg(
                        "No key found (':' missing)",
                        self.nb_line)
                    )
                except errors.MapFileError as e:
                    self.err.append(str(e))
            if self.err:
                for error in self.err:
                    print(error)
                raise errors.ParsingError
        except FileNotFoundError:
            print(errors.MapFileError.msg("File does not exist"))
            sys.exit(0)
        except PermissionError:
            print(errors.MapFileError.msg("Permission denied"))
            sys.exit(0)

    def check_line(self, key: str, info: str) -> None:
        m_start = info.find("[")
        m_end = info.find("]")
        if m_start != -1 and m_end != -1:
            tmp = info.replace(info[m_start:m_end + 1], "")
            parts = tmp.split()
            if (
                (key == "hub" and len(parts) > 3)
                or (key == "connection" and len(parts) > 1)
            ):
                self.err.append(errors.InvalidLineError(self.nb_line))
        else:
            parts = info.split()
            if (
                (key == "hub" and len(parts) > 3)
                or (key == "connection" and len(parts) > 1)
            ):
                self.err.append(errors.InvalidLineError(self.nb_line))

    def parse_key_info(self, key: str, info: str) -> None:
        if key == "nb_drones":
            try:
                if self.nb_drones is None:
                    if int(info) < 1:
                        raise errors.InvalidValue(
                            self.nb_line,
                            "Cant have less than 1 drone"
                        )
                    self.nb_drones = int(info)
                    self.nb_drones_check = 1
                else:
                    raise errors.DoublonError(self.nb_line, key)
            except ValueError:
                raise errors.InvalidValue(
                    self.nb_line,
                    "<nb_drones> value need to be an integer"
                )
        elif key == "start_hub":
            if not self.start_hub:
                self.start_hub = self.parse_hub(info)
                self.start_hub['metadata']['max_drones'] = self.nb_drones
                self.try_position(self.start_hub)
                self.hubs.append(self.start_hub)
            else:
                raise errors.HubError(self.nb_line, "Can't have 2 start_hub")
        elif key == "end_hub":
            if not self.end_hub:
                self.end_hub = self.parse_hub(info)
                self.end_hub['metadata']['max_drones'] = self.nb_drones
                self.try_position(self.end_hub)
                self.hubs.append(self.end_hub)
            else:
                raise errors.HubError(self.nb_line, "Can't have 2 end_hub")
        elif key == "hub":
            tmp_hub = self.parse_hub(info)
            self.try_position(tmp_hub)
            self.hubs.append(tmp_hub)
        elif key == "connection":
            parsed_c = self.parse_connection(info)
            hub1, hub2 = parsed_c["hub_a"], parsed_c["hub_b"]
            for connection in self.connection:
                if {hub1, hub2} == {
                        connection["hub_a"],
                        connection["hub_b"],
                }:
                    name = f"{parsed_c['hub_a']}-{parsed_c['hub_b']}"
                    message = f"Connection already defined earlier <{name}>"
                    self.err.append(errors.ConnectionError(
                        self.nb_line,
                        message
                    ))
            if hub1 not in self.hub_name and hub1 is not None:
                raise errors.HubError(
                    self.nb_line,
                    f"Hub '{hub1}' not defined yet"
                )
            if hub2 not in self.hub_name and hub2 is not None:
                raise errors.HubError(
                    self.nb_line,
                    f"Hub '{hub2}' not defined yet"
                )
            self.connection.append(parsed_c)
        else:
            raise errors.InvalidKeyError(self.nb_line, key)

    def try_position(self, hub_info: dict) -> None:
        try:
            x = int(hub_info["pos_x"])
            y = int(hub_info["pos_y"])
            for verif in self.hubs:
                if x == verif["pos_x"] and y == verif["pos_y"]:
                    self.err.append(errors.HubError(
                        self.nb_line,
                        f"Position <{x}, {y}> already occupied "
                        f"by Hub: {verif['name']}"
                    ))
            hub_info["pos_x"] = int(hub_info["pos_x"])
            hub_info["pos_y"] = int(hub_info["pos_y"])
        except ValueError:
            raise errors.HubError(
                self.nb_line,
                f"Undefined '{hub_info['name']}' hub position"
            )

    def parse_hub(self, line: str) -> dict:
        default_info = {
            "name": "undefined",
            "pos_x": "undefined",
            "pos_y": "undefined"
        }
        default_metadata = {
            "zone": "normal",
            "max_drones": "1",
            "color": "none"
        }
        hub_info: dict[str, Any] = {}
        tmp_line = ""
        metadata_index = line.find("[")
        if metadata_index != -1:
            tmp_line = line[:metadata_index].strip()
            hub_info = {
                key: value
                for key, value
                in zip(["name", "pos_x", "pos_y"], tmp_line.split())
            }
            if hub_info["name"] in self.hub_name:
                self.err.append(errors.HubError(
                    self.nb_line,
                    f"'{hub_info['name']}' already defined earlier"
                ))
            self.hub_name.append(hub_info["name"])
            hub_info["metadata"] = self.parse_metadata(
                hub_info["name"],
                line[metadata_index:],
                default_metadata
            )
            return {**default_info, **hub_info}
        else:
            tmp_line = line.strip()
            hub_info = {
                key: value
                for key, value
                in zip(["name", "pos_x", "pos_y"], tmp_line.split())
            }
            if hub_info["name"] in self.hub_name:
                self.err.append(errors.HubError(
                    self.nb_line,
                    f"'{hub_info['name']}' already defined earlier"
                ))
            self.hub_name.append(hub_info["name"])
            hub_info["metadata"] = default_metadata
            return {**default_info, **hub_info}

    def parse_metadata(
            self,
            name: str,
            info_metadata: str,
            default_metadata: dict
    ) -> dict:
        info: list = [i.split("=") for i in info_metadata.strip("[]").split()]
        verif_format: list
        for verif_format in info:
            if len(verif_format) == 1:
                verif_format.append("undefined")
            elif len(verif_format) == 2 and verif_format[1] == "":
                if verif_format[0] == "zone":
                    print(errors.MapFileError.warning(
                        self.nb_line,
                        f"Value is missing for '{verif_format[0]}', "
                        f"'normal' set by default"
                    ))
                    verif_format[1] = "normal"
                elif verif_format[0] == "max_drones":
                    print(errors.MapFileError.warning(
                        self.nb_line,
                        f"Value is missing for '{verif_format[0]}', "
                        f"'1' set by default"
                    ))
                    verif_format[1] = 1
            elif len(verif_format) > 2:
                info.remove(verif_format)
                self.err.append(errors.MetadataError(
                    self.nb_line,
                    "Typing incorrect, follow <metadata=info>"
                ))
        new_metadata = {
            **default_metadata,
            **{key: value for key, value in info}
        }
        try:
            for key in new_metadata.keys():
                if key not in ["zone", "color", "max_drones"]:
                    self.err.append(errors.MetadataError(
                        self.nb_line,
                        f"Unknown metadata '{key}'"
                    ))
            if (
                "zone" in new_metadata
                and new_metadata["zone"]
                not in ["normal", "blocked", "restricted", "priority"]
            ):
                self.err.append(errors.HubError(
                    self.nb_line,
                    f"Invalid zone_type '{new_metadata['zone']}'"
                ))
            if (
                "color" in new_metadata
                and new_metadata["color"] not in Color.list
            ):
                print(new_metadata["color"])
                print(errors.MapFileError.warning(
                    self.nb_line,
                    f"Unknown color for hub '{name}', "
                    "color set to grey by default"
                ))
                new_metadata["color"] = "gray"
            if "max_drones" in new_metadata:
                new_metadata["max_drones"] = int(new_metadata["max_drones"])
                if new_metadata["max_drones"] < 0:
                    self.err.append(errors.InvalidValue(
                        self.nb_line,
                        "Invalid 'max_drones' value, minimum is 0"
                    ))
        except ValueError:
            self.err.append(errors.InvalidValue(
                self.nb_line,
                "Invalid 'max_drones' value"
            ))
        return new_metadata

    def parse_connection(self, line: str) -> dict:
        default_metadata = {
            "max_link_capacity": 1
        }
        metadata_index = line.find("[")
        invalid_data = []
        if metadata_index != -1:
            link = line[:metadata_index].strip().split("-")
            if len(link) != 2 or "" in link:
                self.err.append(errors.ConnectionError(
                    self.nb_line,
                    "Connection invalid, follow <from-to>"
                ))
                link = ["None", "None"]
            info = [
                i.split("=")
                for i in line[metadata_index:].strip("[]").split()
            ]
            for verif_format in info:
                if len(verif_format) == 1:
                    self.err.append(errors.MetadataError(
                        self.nb_line,
                        "Missing value after metadata key, "
                        "follow <metadata=value>"
                    ))
                    verif_format.append("undefined")
                elif len(verif_format) == 2 and verif_format[1] == "":
                    print(errors.MapFileError.warning(
                        self.nb_line,
                        f"Value is missing for '{verif_format[0]}', "
                        "'1' set by default"
                    ))
                    verif_format[1] = "None"
                elif len(verif_format) > 2:
                    info.remove(verif_format)
                    self.err.append(errors.MetadataError(
                        self.nb_line,
                        "Typing incorrect, follow <metadata=info>"
                    ))
            metadata: dict[str, Any] = {key: value for key, value in info}
            try:
                for check_metadata in metadata.keys():
                    if check_metadata != "max_link_capacity":
                        invalid_data.append(check_metadata)
                if len(invalid_data):
                    self.err.append(errors.MetadataError(
                        self.nb_line,
                        f"Unknown metadata '{invalid_data}'"
                    ))
                metadata["max_link_capacity"] = int(
                    metadata["max_link_capacity"]
                )
                if metadata["max_link_capacity"] < 0:
                    self.err.append(errors.InvalidValue(
                        self.nb_line,
                        "Invalid 'max_link_capacity' value, minimum is 0"))
            except ValueError:
                self.err.append(errors.ConnectionError(
                    self.nb_line,
                    "Value need to be an integer for 'max_link_capacity'"
                ))
            return {"hub_a": link[0], "hub_b": link[1], "metadata": metadata}
        else:
            link = line.strip().split("-")
            if len(link) != 2 or "" in link:
                self.err.append(errors.ConnectionError(
                    self.nb_line,
                    "Connection invalid, follow <from-to>"
                ))
                link = ["None", "None"]
            return {
                "hub_a": link[0],
                "hub_b": link[1],
                "metadata": default_metadata
            }
    #
    # def verif_all(self) -> None:
    #     if "None" in self.start_hub.values():
    #         self.is_valid = False
    #     if "None" in self.end_hub.values():
    #         self.is_valid = False
    #     if "None" in self.start_hub.values():
    #         self.is_valid = False
