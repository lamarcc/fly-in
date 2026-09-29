from map import Map, Hub, Connection
from typing import Any


class Drone():
    """A drone moving through the simulation.

    Each drone follows a predefined path from the start hub to the end hub,
    taking into account the capacities of hubs and connections.
    """

    def __init__(self, number: int, map: Map, road: list) -> None:
        """Initialize a drone with its path.

        Args:
            number: Unique drone number.
            map: Reference to the simulation map.
            road: List of hubs that make up the drone's path.
        """
        self.number = number
        self.map = map
        self.pos = map.start_hub
        self.finished = False
        self.count = 0
        self.path = list(road)

    def move_to(self) -> None:
        """Perform the drone's movement to the next position.

        Handles capacity rules and different zone types. If the drone cannot
        move forward (insufficient capacity), it stays in place and increments
        the waiting counter.
        """
        if self.pos == self.map.end_hub:
            return
        next_move = self.path[1]
        if isinstance(self.pos, Hub) and next_move.zone_type == "restricted":
            if not self.check_connection_capacity(next_move):
                self.count += 1
                return
            connection = self.pos.get_this_connection(next_move)
            connection.passed += 1
            self.move(connection)
            return
        if isinstance(self.pos, Connection):
            if not next_move.check_capacity():
                self.count += 1
                return
            self.move(next_move)
            return
        if not next_move.check_capacity():
            self.count += 1
            return
        if not self.check_connection_capacity(next_move):
            self.count += 1
            return
        connection = self.pos.get_this_connection(next_move)
        connection.passed += 1
        self.move(next_move)
        self.count += 1

    def move(self, destination: Hub | Connection) -> None:
        """Move the drone to a destination.

        Updates the occupation of the current and destination hubs, then
        removes the destination from the path if it is a hub.

        Args:
            destination: The destination hub or connection.
        """
        self.pos.occupied -= 1
        self.pos = destination
        self.pos.occupied += 1
        if isinstance(self.pos, Connection):
            return
        self.path.remove(self.pos)

    def check_connection_capacity(
        self, destination: Hub | Connection
    ) -> Any:
        """Check connection to destination can accept the drone.

        Args:
            destination: The hub the drone wants to move toward.

        Returns:
            bool: True if connection has available capacity, else False.
        """
        if self.pos.is_connected_to(destination):
            connection = self.pos.get_this_connection(destination)
            return connection.passed < connection.max_capacity
        return False
