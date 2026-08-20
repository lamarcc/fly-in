from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Tuple, Any
from .parsing import Parse
from enum import Enum


class Simulation():
    def __init__(self):
        self.map = Map()
        self.parse = Parse()
        self.is_running = False
        self.drones_finished = 0

    def init_hubs(self, data: Any):
        for info in data:
            hub = Hub(info["name"], info["pos_x"], info["pos_y"], info["metadata"])
            self.map.hubs[hub.name] = hub

    def init_connections(self, data: Any):
        for info in data:
            connection = Connection(self.map.hubs[info["hub_a"]], self.map.hubs[info["hub_b"]], info["metadata"])
            self.map.connections.append(connection)
        ## TODO: Add all connections to specify hubs (hubs.connection list, need to add all object of the differents hub)

    def init_window(self):
        pass ## TODO: need to choose a visualizer for the simulation

    def init(self):
        self.map.nb_drones = self.parse.nb_drones
        self.init_hubs(self.parse.hubs)
        self.init_connections(self.parse.connection)
        self.map.nb_drones = self.parse.nb_drones
        self.map.start_hub = Hub(self.parse.start_hub["name"], self.parse.start_hub["pos_x"], self.parse.start_hub["pos_y"], self.parse.start_hub["metadata"])
        self.map.end_hub = Hub(self.parse.end_hub["name"], self.parse.end_hub["pos_x"], self.parse.end_hub["pos_y"], self.parse.end_hub["metadata"])

    def run(self):
        pass


class Map():
    def __init__(self):
        self.map = [[]]
        self.nb_drones = 0
        self.start_hub = None
        self.end_hub = None
        self.hubs = {}
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
    def __init__(self, hub_a: Hub, hub_b: Hub, data: dict):
        self.hub_a = hub_a
        self.hub_b = hub_b
        self.max_link_capacity = data["max_link_capacity"]


class Zone(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"
