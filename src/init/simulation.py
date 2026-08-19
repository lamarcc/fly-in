from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Tuple, Any
from .parsing import Parse
from enum import Enum


class Simulation():
    def __init__(self):
        self.map = Map()
        self.running = 0
        self.drones_finished = 0

    def init_map(self, data: Any):
        pass

    def init_hubs(self, data: Any):
        for hub in data:
            self.map.hubs.append(Hub(hub["name"], hub["pos_x"], hub["pos_y"], hub["metadata"]))

    def init_connections(self, data: Any):
        for connection in data:
            self.map.connections.append(Connection(connection))

    def start(self):
        pass

    def init_window(self):
        pass


class Map():
    def __init__(self):
        self.map = [[]]
        self.nb_drones = 0
        self.start_hub = None
        self.end_hub = None
        self.hubs = []
        self.connections = []


class Hub():
    def __init__(self, name: str, x: int, y: int, metadata: dict):
        self.name = name
        self.x_pos = x
        self.y_pos = y
        self.metadata = metadata
        self.connections = []

    def update_metadata(self, data: dict):
        self.metadata = data

    def get_connections(self):
        return self.connections


class Connection():
    def __init__(self, data: dict):
        self.hub_a = data["connection"][0]
        self.hub_b = data["connection"][1]
        self.max_link_capacity = data["metadata"]


class Zone(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"
