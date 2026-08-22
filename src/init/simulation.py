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
        self.map.start_hub = Hub(self.parse.start_hub["name"], self.parse.start_hub["pos_x"], self.parse.start_hub["pos_y"], self.parse.start_hub["metadata"])
        self.map.end_hub = Hub(self.parse.end_hub["name"], self.parse.end_hub["pos_x"], self.parse.end_hub["pos_y"], self.parse.end_hub["metadata"])
        self.parse.hubs.remove(self.parse.start_hub)
        self.parse.hubs.remove(self.parse.end_hub)
        self.map.hubs[self.parse.start_hub["name"]] = self.map.start_hub
        for info in data:
            hub = Hub(info["name"], info["pos_x"], info["pos_y"], info["metadata"])
            self.map.hubs[hub.name] = hub
        self.map.hubs[self.parse.end_hub["name"]] = self.map.end_hub

    def init_connections(self, data: Any):
        for info in data:
            connection = Connection(self.map.hubs[info["hub_a"]], self.map.hubs[info["hub_b"]], info["metadata"])
            self.map.connections.append(connection)
        for connection in self.map.connections:
            connection.hub_a.connected_to.append(connection.hub_b)
            connection.hub_b.connected_to.append(connection.hub_a)

    def init_map(self):
        all_coordinate = [(pos.pos_x, pos.pos_y) for pos in self.map.hubs.values()]
        max_x = 0
        max_y = 0
        for x, y in all_coordinate:
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
        zones = [zone for zone in self.map.hubs.values()]
        for y in range(max_y + 1):
            tmp = []
            for x in range(max_x + 1):
                tmp.append(0)
            self.map.map.append(tmp)
        for z in zones:
            if z.zone_type == "normal":
                self.map.map[z.pos_y][z.pos_x] = 1
            elif z.zone_type == "priority":
                self.map.map[z.pos_y][z.pos_x] = 2
            elif z.zone_type == "restricted":
                self.map.map[z.pos_y][z.pos_x] = 3
            elif z.zone_type == "blocked":
                self.map.map[z.pos_y][z.pos_x] = 4
        for x in reversed(self.map.map):
            print(x)

    def init_window(self):
        pass ## TODO: need to choose a visualizer for the simulation

    def init(self):
        self.map.nb_drones = self.parse.nb_drones
        self.init_hubs(self.parse.hubs)
        self.init_connections(self.parse.connection)
        self.init_map()

    def run(self):
        p = Path()
        drone = Drone(1)
        p.path(self.map, drone)


class Map():
    def __init__(self):
        self.map = []
        self.nb_drones = 0
        self.start_hub = None
        self.end_hub = None
        self.hubs = {}
        self.connections = []


class Hub():
    def __init__(self, name: str, x: int, y: int, metadata: dict):
        self.name = name
        self.pos_x = x
        self.pos_y = y
        self.connected_to = []
        self.zone_type = metadata["zone"]
        self.color = metadata["color"]
        self.max_capacity = metadata["max_drones"]

    def get_position(self):
        return (self.pos_x, self.pos_y)

    def get_type(self):
        return (self.type)

    def get_connections(self):
        return self.connected_to


class Connection():
    def __init__(self, hub_a: Hub, hub_b: Hub, data: dict):
        self.hub_a = hub_a
        self.hub_b = hub_b
        self.max_capacity = data["max_link_capacity"]


class ZoneType(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class Drone():
    def __init__(self, number):
        self.number = number
        self.path = []
        self.finished = False


class Path():
    def __init__(self):
        pass

    def path(self, map, drone):
        start = map.start_hub
        end = map.end_hub
        allowed = []
        ndone = []
        d = {}
        r_d = {}
        tour = 0
        path = {}
        for hub in map.hubs.values():
            if hub.zone_type == "blocked":
                continue
            allowed.append(hub)
            if hub == start:
                ndone.append((hub, 0))
                d[start] = 0
            else:
                ndone.append((hub, float('inf')))
                d[hub] = float('inf')
        while len(d.keys()) != 0:
            lowest = min([v for k, v in d.items()])
            r_d = {v: k for k, v in d.items()}
            hub = r_d[lowest]
            if hub == end:
                print(d[hub])
            for hub_to in hub.connected_to:
                if hub_to not in d.keys():
                    continue
                print("hub actual")
                print(hub.name)
                print("hub_to verified")
                print(hub_to.name)
                if hub_to.zone_type == "normal":
                    if d[hub_to] == float('inf'):
                        d[hub_to] = 0
                    d[hub_to] += d[hub] + 1
                elif hub_to.zone_type == "priority":
                    if d[hub_to] == float('inf'):
                        d[hub_to] = 0
                    d[hub_to] += d[hub] + 0.5
                elif hub_to.zone_type == "restricted":
                    if d[hub_to] == float('inf'):
                        d[hub_to] = 0
                    d[hub_to] += d[hub] + 2
                print(d[hub_to])
                path[hub_to] = hub
            d.pop(hub)
        for key, value in path.items():
            print(key.name)
            print(value.name)
        ## TODO: 
        ## - Modifier le cas ou le meme hub est verifier plusieurs fois dans la boucle, 
        ## (dernier tour, goal est verifier plusieurs fois donc sa valeur change plusieurs 
        ## fois alors que le goal a deja ete trouve, la valeur doit changer que si la nouvelle est plus petite que l' ancienne)
        ## - Trouver un moyen de sauvegarder le path petit a petit
        ## - Ameliorer l' algo pour les max_drones et max_link_capacity plus tard quand plusieurs drone seront ajoute
