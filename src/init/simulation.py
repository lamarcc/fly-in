from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Tuple
from .parser import Parse
from enum import Enum


class Map():
    def __init__(self):
        self.nb_drones = 0
        self.start_hub = None
        self.end_hub = None
        self.hubs = []
        self.connections = []


class Hub():
    def __init__(self, name: str, x: int, y: int):
        self.name = name
        self.x_pos = x
        self.y_pos = y
        self.metadata = {
            "zone": Zone.NORMAL,
            "max_drones": 1,
            "color": "grey"
        }
        self.connection = []

    def update_metadata(self, data: dict):
        self.metadata = data


class Connection():
    def __init__(self, data: dict):
        self.


class Zone(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"
