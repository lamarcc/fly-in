from .map import Map, Hub, Connection
from typing import Any


class Drone():
    def __init__(self, number: int, map: Map, road: list) -> None:
        self.number = number
        self.map = map
        self.pos = map.start_hub
        self.finished = False
        self.count = 0
        self.path = list(road)

    def move_to(self) -> None:
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
        self.pos.occupied -= 1
        self.pos = destination
        self.pos.occupied += 1
        if isinstance(self.pos, Connection):
            return
        self.path.remove(self.pos)

    def check_connection_capacity(self, destination: Hub | Connection) -> Any | bool:
        if self.pos.is_connected_to(destination):
            connection = self.pos.get_this_connection(destination)
            return connection.passed < connection.max_capacity
        return False
