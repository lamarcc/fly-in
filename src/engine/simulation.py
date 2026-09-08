from __future__ import annotations
from parser import Parse
from typing import Any
import render
import engine


class Simulation():
    def __init__(self) -> None:
        self.map = engine.Map()
        self.parser = Parse()
        self.visualizer = render.Visualizer(self.map, self)
        self.is_running = False
        self.drones = []
        self.drones_finished = []
        self.drones_pos = {}

    def init_drones(self, path: list) -> None:
        for i in range(1, self.map.nb_drones + 1):
            drone = engine.Drone(i, self.map, path)
            self.drones.append(drone)

    def init_hubs(self, data: Any) -> None:
        self.map.start_hub = engine.Hub(self.map, self.parser.start_hub["name"], self.parser.start_hub["pos_x"], self.parser.start_hub["pos_y"], self.parser.start_hub["metadata"])
        self.map.end_hub = engine.Hub(self.map, self.parser.end_hub["name"], self.parser.end_hub["pos_x"], self.parser.end_hub["pos_y"], self.parser.end_hub["metadata"])
        self.parser.hubs.remove(self.parser.start_hub)
        self.parser.hubs.remove(self.parser.end_hub)
        self.map.hubs[self.parser.start_hub["name"]] = self.map.start_hub
        for info in data:
            hub = engine.Hub(self.map, info["name"], info["pos_x"], info["pos_y"], info["metadata"])
            self.map.hubs[hub.name] = hub
        self.map.hubs[self.parser.end_hub["name"]] = self.map.end_hub

    def init_connections(self, data: Any) -> None:
        for info in data:
            hub_a = self.map.hubs[info['hub_a']]
            hub_b = self.map.hubs[info['hub_b']]
            name = f'{hub_a.name}-{hub_b.name}'
            connection = engine.Connection(name, hub_a, hub_b, info["metadata"])
            self.map.connections[name] = connection
        for connection in self.map.connections.values():
            connection.hub_a.connected_to.append(connection.hub_b)
            connection.hub_b.connected_to.append(connection.hub_a)

    def init(self) -> None:
        self.map.nb_drones = self.parser.nb_drones
        self.init_hubs(self.parser.hubs)
        self.init_connections(self.parser.connection)

    def reset_passed_connection(self) -> None:
        for connection in self.map.connections.values():
            connection.passed = 0

    def print_movement(self, drones_movements: dict) -> None:
        i = 1
        while i != len(drones_movements.keys()):
            for drone, hub in drones_movements[f'Lap{i}'].items():
                if drones_movements[f'Lap{i}'][drone] != drones_movements[f'Lap{i-1}'][drone]:
                    print(f'D{drone}-{hub.name}', end=" ")
            print()
            i += 1

    def move_drones(self) -> None:
        for drone in self.drones:
            drone.move_to()
            if drone.pos == self.map.end_hub:
                self.drones_finished.append(drone)

    def flyin(self, path: list) -> None:
        lap = 0
        self.drones_pos[f'Lap{lap}'] = {drone.number: drone.pos for drone in self.drones}
        while len(set(self.drones_finished)) < self.map.nb_drones:
            self.reset_passed_connection()
            self.move_drones()
            lap += 1
            self.drones_pos[f'Lap{lap}'] = {drone.number: drone.pos for drone in self.drones}
        self.print_movement(self.drones_pos)

    def run(self) -> None:
        pathfinder = engine.Pathfinding(self.map)
        path = pathfinder.find_path()
        self.init_drones(path)
        self.flyin(path)
        self.visualizer.create_window(self.drones_pos)
