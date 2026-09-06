from enum import Enum

class Map():
    def __init__(self):
        self.map = []
        self.nb_drones = 0
        self.start_hub = None
        self.end_hub = None
        self.hubs = {}
        self.connections = {}


class Hub():
    def __init__(self, map, name: str, x: int, y: int, metadata: dict):
        self.name = name
        self.map = map
        self.pos_x = x
        self.pos_y = y
        self.connected_to = []
        self.zone_type = metadata["zone"]
        self.color = metadata["color"]
        self.max_capacity = metadata["max_drones"]
        self.occupied = 0

    def get_connections(self):
        return self.connected_to

    def get_pos(self):
        return (self.pos_x, self.pos_y)

    def check_capacity(self):
        return (self.occupied + 1 <= self.max_capacity)

    def is_connected_to(self, hub):
        return (hub in self.connected_to)

    def get_this_connection(self, hub):
        return self.map.connections[f'{self.name}-{hub.name}'] or self.map.connections[f'{hub.name}-{self.name}']


class Connection():
    def __init__(self, name, hub_a: Hub, hub_b: Hub, data: dict):
        self.name = name
        self.hub_a = hub_a
        self.hub_b = hub_b
        self.max_capacity = data["max_link_capacity"]
        self.occupied = 0
        self.passed = 0

    def check_capacity(self):
        return (self.occupied + 1 <= self.max_capacity)


class ZoneType():
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"
