from __future__ import annotations
from parser import Parse
from typing import Tuple, Any
import render
import engine


class Simulation():
    def __init__(self):
        self.map = engine.Map()
        self.parser = Parse()
        self.visualizer = render.Visualizer(self.map, self)
        self.is_running = False
        self.drones = []
        self.drones_finished = []
        self.drones_pos = {}

    def init_drones(self, road):
        for i in range(1, self.map.nb_drones + 1):
            drone = engine.Drone(i, self.map, road)
            self.drones.append(drone)

    def init_hubs(self, data: Any):
        self.map.start_hub = engine.Hub(self.map, self.parser.start_hub["name"], self.parser.start_hub["pos_x"], self.parser.start_hub["pos_y"], self.parser.start_hub["metadata"])
        self.map.end_hub = engine.Hub(self.map, self.parser.end_hub["name"], self.parser.end_hub["pos_x"], self.parser.end_hub["pos_y"], self.parser.end_hub["metadata"])
        self.parser.hubs.remove(self.parser.start_hub)
        self.parser.hubs.remove(self.parser.end_hub)
        self.map.hubs[self.parser.start_hub["name"]] = self.map.start_hub
        for info in data:
            hub = engine.Hub(self.map, info["name"], info["pos_x"], info["pos_y"], info["metadata"])
            self.map.hubs[hub.name] = hub
        self.map.hubs[self.parser.end_hub["name"]] = self.map.end_hub

    def init_connections(self, data: Any):
        for info in data:
            hub_a = self.map.hubs[info['hub_a']]
            hub_b = self.map.hubs[info['hub_b']]
            name = f'{hub_a.name}-{hub_b.name}'
            connection = engine.Connection(name, hub_a, hub_b, info["metadata"])
            self.map.connections[name] = connection
        for connection in self.map.connections.values():
            connection.hub_a.connected_to.append(connection.hub_b)
            connection.hub_b.connected_to.append(connection.hub_a)

    def init(self):
        self.map.nb_drones = self.parser.nb_drones
        self.init_hubs(self.parser.hubs)
        self.init_connections(self.parser.connection)

    def run(self):
        p = engine.Pathfinding(self.map)
        road = p.find_path()
        self.init_drones(road)
        self.flyin(road)

    def flyin(self, path):
        lap = 0
        self.drones_pos[f'Lap{lap}'] = {drone.number: drone.pos for drone in self.drones}
        while len(set(self.drones_finished)) < self.map.nb_drones:
            for connection in self.map.connections.values():
                connection.passed = 0
            for drone in self.drones:
                drone.move_to()
                if drone.pos == self.map.end_hub:
                    self.drones_finished.append(drone)
            lap += 1
            self.drones_pos[f'Lap{lap}'] = {drone.number: drone.pos for drone in self.drones}
        self.visualizer.create_window(self.drones_pos)
