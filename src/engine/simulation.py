from __future__ import annotations
from parser import Parse
from typing import Any
import engine


class Simulation():
    """Manages the full execution of the drone simulation.

    Coordinates parsing, initialization, movement simulation,
    and visualization of the results.
    """

    def __init__(self) -> None:
        """Initialize a new simulation with its components."""
        import render
        self.map: engine.Map = engine.Map()
        self.parser: Parse = Parse()
        self.visualizer: render.Visualizer = render.Visualizer(self.map, self)
        self.is_running: bool = False
        self.drones: list = []
        self.drones_finished: list = []
        self.drones_pos: dict = {}

    def init_drones(self, path: list) -> None:
        """Create all drones for the simulation.

        Args:
            path: The path all drones must follow.
        """
        for i in range(1, self.map.nb_drones + 1):
            drone = engine.Drone(i, self.map, path)
            self.drones.append(drone)

    def init_hubs(self, data: Any) -> None:
        """Initialize all hubs in the simulation.

        Creates the start hub, end hub, and all intermediate hubs by attaching
        them to the map.

        Args:
            data: List of intermediate hubs parsed from the file.
        """
        self.map.start_hub = engine.Hub(
            self.map,
            self.parser.start_hub["name"],
            self.parser.start_hub["pos_x"],
            self.parser.start_hub["pos_y"],
            self.parser.start_hub["metadata"]
        )
        self.map.end_hub = engine.Hub(
            self.map,
            self.parser.end_hub["name"],
            self.parser.end_hub["pos_x"],
            self.parser.end_hub["pos_y"],
            self.parser.end_hub["metadata"]
        )
        self.parser.hubs.remove(self.parser.start_hub)
        self.parser.hubs.remove(self.parser.end_hub)
        self.map.hubs[self.parser.start_hub["name"]] = self.map.start_hub
        for info in data:
            hub = engine.Hub(
                self.map,
                info["name"],
                info["pos_x"],
                info["pos_y"],
                info["metadata"]
            )
            self.map.hubs[hub.name] = hub
        self.map.hubs[self.parser.end_hub["name"]] = self.map.end_hub

    def init_connections(self, data: Any) -> None:
        """Initialize all connections between hubs.

        Args:
            data: List of parsed connections.
        """
        for info in data:
            hub_a = self.map.hubs[info['hub_a']]
            hub_b = self.map.hubs[info['hub_b']]
            name = f'{hub_a.name}-{hub_b.name}'
            connection = engine.Connection(
                name,
                hub_a,
                hub_b,
                info["metadata"]
            )
            self.map.connections[name] = connection
        for connection in self.map.connections.values():
            connection.hub_a.connected_to.append(connection.hub_b)
            connection.hub_b.connected_to.append(connection.hub_a)

    def init(self) -> None:
        """Initialize the full simulation from the parsed data."""
        self.map.nb_drones = self.parser.nb_drones
        self.init_hubs(self.parser.hubs)
        self.init_connections(self.parser.connection)

    def reset_passed_connection(self) -> None:
        """Reset the counter of drones that passed through each connection.

        Called at each lap to reapply the capacity rules.
        """
        for connection in self.map.connections.values():
            connection.passed = 0

    def print_movement(self, drones_movements: dict) -> None:
        """Display the history of drone movements.

        Args:
            drones_movements: Dictionary containing positions for each lap.
        """
        i = 1
        while i != len(drones_movements.keys()):
            for drone, hub in drones_movements[f'Lap{i}'].items():
                if (
                    drones_movements[f'Lap{i}'][drone]
                    != drones_movements[f'Lap{i-1}'][drone]
                ):
                    print(f'D{drone}-{hub.name}', end=" ")
            print()
            i += 1

    def move_drones(self) -> None:
        """Perform a move for all unfinished drones.

        Updates the list of drones that have reached the destination.
        """
        for drone in self.drones:
            drone.move_to()
            if drone.pos == self.map.end_hub:
                self.drones_finished.append(drone)

    def flyin(self, path: list) -> None:
        """Execute the main simulation loop.

        Repeats drone motion until all reach the destination while recording
        the position history.

        Args:
            path: The path to follow for the drones.
        """
        lap = 0
        self.drones_pos[f'Lap{lap}'] = {
            drone.number: drone.pos
            for drone in self.drones
        }
        while len(set(self.drones_finished)) < self.map.nb_drones:
            self.reset_passed_connection()
            self.move_drones()
            lap += 1
            self.drones_pos[f'Lap{lap}'] = {
                drone.number: drone.pos
                for drone in self.drones
            }
        self.print_movement(self.drones_pos)

    def run(self) -> None:
        """Run the full simulation: pathfinding, initialization, and execution."""
        pathfinder = engine.Pathfinding(self.map)
        path = pathfinder.find_path()
        self.init_drones(path)
        self.flyin(path)
        self.visualizer.create_window(self.drones_pos)
