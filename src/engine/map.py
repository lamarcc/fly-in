from __future__ import annotations
from typing import Tuple, Any


class Map():
    """Represents the structure of a simulation map.

    Contains all hubs (nodes) and connections (edges) that make up the network
    through which drones must travel.
    """

    def __init__(self) -> None:
        """Initialize an empty map."""
        self.nb_drones: int = 0
        self.start_hub: Any = None
        self.end_hub: Any = None
        self.hubs: dict = {}
        self.connections: dict = {}


class Hub():
    """Represents a node (hub) in the simulation map.

    A hub has a position, capacity, zone type, and connections to other hubs.
    """

    def __init__(self, map: Map, name: str, x: int, y: int, metadata: dict):
        """Initialize a hub with its configuration.

        Args:
            map: Reference to the parent map.
            name: Unique name of the hub.
            x: X coordinate of the position.
            y: Y coordinate of the position.
            metadata: Dictionary containing zone, color, and max_drones.
        """
        self.name: str = name
        self.map: Map = map
        self.pos_x: int = x
        self.pos_y: int = y
        self.connected_to: list[Hub] = []
        self.zone_type: dict = metadata["zone"]
        self.color: str = metadata["color"]
        self.max_capacity: int = metadata["max_drones"]
        self.occupied: int = 0

    def get_connections(self) -> list:
        """Return the list of hubs this hub is connected to.

        Returns:
            list: The list of connected hubs.
        """
        return self.connected_to

    def get_pos(self) -> Tuple[int, int]:
        """Return the hub coordinates.

        Returns:
            Tuple[int, int]: The position tuple (x, y).
        """
        return (self.pos_x, self.pos_y)

    def check_capacity(self) -> bool:
        """Check whether the hub can accept one more drone.

        Returns:
            bool: True if capacity has not been exceeded, otherwise False.
        """
        return (self.occupied + 1 <= self.max_capacity)

    def is_connected_to(self, hub: Hub) -> bool:
        """Check whether this hub is directly connected to another.

        Args:
            hub: The hub to check.

        Returns:
            bool: True if the two hubs are connected, otherwise False.
        """
        return (hub in self.connected_to)

    def get_this_connection(self, hub: Hub) -> Any:
        """Retrieve the Connection object linking this hub to another.

        Args:
            hub: The destination hub.

        Returns:
            Connection: The connection object between the two hubs.
        """
        if f'{self.name}-{hub.name}' in self.map.connections:
            return self.map.connections[f'{self.name}-{hub.name}']
        else:
            return self.map.connections[f'{hub.name}-{self.name}']


class Connection():
    """Represents a connection (edge) between two hubs.

    Tracks the connection capacity and the number of drones crossing it.
    """

    def __init__(self, name: str, hub_a: Hub, hub_b: Hub, data: dict) -> None:
        """Initialize a connection between two hubs.

        Args:
            name: Unique identifier of the connection.
            hub_a: First hub connected.
            hub_b: Second hub connected.
            data: Dictionary containing max_link_capacity.
        """
        self.name = name
        self.hub_a = hub_a
        self.hub_b = hub_b
        self.max_capacity = data["max_link_capacity"]
        self.occupied = 0
        self.passed = 0

    def check_capacity(self) -> Any:
        """Check whether the connection can accept one more drone.

        Returns:
            bool: True if capacity has not been exceeded, otherwise False.
        """
        return (self.occupied + 1 <= self.max_capacity)


class ZoneType():
    """Enumeration of the possible zone types for hubs.

    Attributes:
        NORMAL: Normal zone with a cost of 1.
        BLOCKED: Blocked zone, inaccessible to drones.
        RESTRICTED: Restricted zone with a cost of 2.
        PRIORITY: Priority zone with a cost of 0.5.
    """
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"
