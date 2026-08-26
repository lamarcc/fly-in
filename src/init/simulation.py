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
        self.drones = []
        self.drones_finished = 0

    def init_drones(self, road):
        # drones = []
        for i in range(1, self.map.nb_drones + 1):
            self.drones.append(Drone(i, self.map, road))
            # self.drones[drones[i-1]] = self.map.start_hub
        # for k, v in self.drones.items():
        #     print(f"{k}: {v.name}")

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
        p = Pathfinding(self.map)
        road = p.find_path()
        self.init_drones(road)
        self.flyin(road)

    def flyin(self, path):
        tour = 0
        while self.drones_finished != self.map.nb_drones:
            for drone in self.drones:
                if drone.finished == True:
                    self.drones_finished += 1
                    print(drone.count)
                    continue
                else:
                    drone.go_to()


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
        self.occupied = 0

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
    def __init__(self, number, map, road):
        self.number = number
        self.map = map
        self.pos = map.start_hub
        self.finished = False
        self.count = 0
        self.path = road

    def go_to(self):
        if self.path[1] in self.pos.connected_to:
            if self.path[1].occupied:
                self.count += 1
                return
            self.occupied = 0
            self.pos = self.path[1]
            self.pos.occupied = 1
            self.count += 1
            if self.pos == self.map.end_hub:
                self.finished = True
                return
            self.path.remove(self.pos)


class Pathfinding():
    def __init__(self, map):
        self.start = map.start_hub
        self.end = map.end_hub
        self.path = {}
        self.zone = {}
        for hub in map.hubs.values():
            if hub.zone_type == "blocked":
                continue
            if hub == self.start:
                self.zone[self.start] = 0
            else:
                self.zone[hub] = float('inf')

    def find_path(self):
        r_zone = {}
        while len(self.zone.keys()) != 0:
            hub = self.get_lowest_hub()
            for hub_to in hub.connected_to:
                if hub_to not in self.zone.keys():
                    continue
                cost = self.get_cost(hub_to, hub)
                if cost:
                    self.zone[hub_to] = cost
                    self.path[hub_to] = hub
            self.zone.pop(hub)
        return self.get_full_path()
        # return self.path

    def get_cost(self, hub_to, actual_hub):
        if hub_to.zone_type == "normal":
            if self.zone[actual_hub] + 1 < self.zone[hub_to]:
                return self.zone[actual_hub] + 1
        elif hub_to.zone_type == "priority":
            if self.zone[actual_hub] + 0.5 < self.zone[hub_to]:
                return self.zone[actual_hub] + 0.5
        elif hub_to.zone_type == "restricted":
            if self.zone[actual_hub] + 2 < self.zone[hub_to]:
                return self.zone[actual_hub] + 2
        
    def get_full_path(self):
        hub = self.end
        path = [hub]
        t = []
        while hub != self.start:
            hub = self.path[hub]
            path.append(hub)
        for i in reversed(path):
            t.append(i)
        return t

    def get_lowest_hub(self):
        lowest_cost = min([v for k, v in self.zone.items()])
        r_dict = {v: k for k, v in self.zone.items()}
        return r_dict[lowest_cost]
