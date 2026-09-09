from __future__ import annotations
from enum import Enum
from typing import Tuple, Any

class Map():
    def __init__(self) -> None:
        self.nb_drones: int = 0
        self.start_hub: Any = None
        self.end_hub: Any = None
        self.hubs: dict = {}
        self.connections: dict = {}


class Hub():
    def __init__(self, map: Map, name: str, x: int, y: int, metadata: dict):
        self.name: str = name
        self.map: Map = map
        self.pos_x: int = x
        self.pos_y: int = y
        self.connected_to: list[Hub] = []
        self.zone_type: dict = metadata["zone"]
        self.color: str = metadata["color"]
        self.max_capacity: int = metadata["max_drones"]
        self.occupied: int = 0

    def get_connections(self) -> list:
        return self.connected_to

    def get_pos(self) -> Tuple[int, int]:
        return (self.pos_x, self.pos_y)

    def check_capacity(self) -> bool:
        return (self.occupied + 1 <= self.max_capacity)

    def is_connected_to(self, hub) -> bool:
        return (hub in self.connected_to)

    def get_this_connection(self, hub) -> Any:
        if f'{self.name}-{hub.name}' in self.map.connections:
            return self.map.connections[f'{self.name}-{hub.name}']
        else:
            return self.map.connections[f'{hub.name}-{self.name}']


class Connection():
    def __init__(self, name: str, hub_a: Hub, hub_b: Hub, data: dict) -> None:
        self.name = name
        self.hub_a = hub_a
        self.hub_b = hub_b
        self.max_capacity = data["max_link_capacity"]
        self.occupied = 0
        self.passed = 0

    def check_capacity(self) -> Any:
        return (self.occupied + 1 <= self.max_capacity)


class ZoneType():
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"
