from parser.errors import Colors
from .map import Map, Hub, ZoneType
from typing import Any


class PathfindingError(Exception):
    """Exception raised when no path is found in the map."""

    def __init__(self, message: str) -> None:
        """Initialize the exception with an error message.

        Args:
            message: Description of the pathfinding error.
        """
        self.message = message

    def __str__(self) -> Any:
        """Return the formatted exception message."""
        error_type = (
                f'{Colors.FAIL}'
                f'{Colors.BOLD}'
                f'[PathfindingError] '
                f'{Colors.ENDC}'
                f'{Colors.BOLD}'
        )
        return error_type + self.message + Colors.ENDC


class Pathfinding():
    """Implements the modified Dijkstra algorithm to find the optimal path.

    Takes zone types (normal, priority, restricted, blocked) into account,
    which affect the path cost.
    """

    def __init__(self, map: Map) -> None:
        """Initialize the pathfinding algorithm.

        Args:
            map: The map to search for a path on.
        """
        self.start: Hub = map.start_hub
        self.end: Hub = map.end_hub
        self.path: dict = {}
        self.zone: dict = {}
        self.path_found: bool = False
        for hub in map.hubs.values():
            if hub.zone_type == "blocked":
                continue
            if hub == self.start:
                self.zone[self.start] = 0
            else:
                self.zone[hub] = float('inf')

    def find_path(self) -> list:
        """Find the optimal path from the start hub to the end hub.

        Uses Dijkstra's algorithm with costs depending on the zone type.

        Returns:
            list: List of hubs forming the optimal path.

        Raises:
            PathfindingError: If no valid path exists.
        """
        while len(self.zone.keys()) != 0:
            hub = self.get_lowest_hub()
            for hub_to in hub.connected_to:
                if hub_to not in self.zone.keys():
                    continue
                if hub_to.get_this_connection(hub).max_capacity == 0:
                    continue
                if hub_to.max_capacity == 0:
                    continue
                cost = self.get_cost(hub_to, hub)
                if cost:
                    self.zone[hub_to] = cost
                    self.path[hub_to] = hub
            self.zone.pop(hub)
        full_path = self.get_full_path()
        if self.path_found is False:
            raise PathfindingError("No valid path found")
        return full_path

    def get_cost(self, hub_to: Hub, actual_hub: Hub) -> Any:
        """Calculate the cost of moving to a hub based on the zone type.

        Costs:
        - NORMAL: 1
        - PRIORITY: 0.5
        - RESTRICTED: 2

        Args:
            hub_to: The hub to calculate the cost for.
            actual_hub: The current hub.

        Returns:
            float: The new path cost, or None if no improvement is made.
        """
        if hub_to.zone_type == ZoneType.NORMAL:
            if self.zone[actual_hub] + 1 < self.zone[hub_to]:
                return self.zone[actual_hub] + 1
        elif hub_to.zone_type == ZoneType.PRIORITY:
            if self.zone[actual_hub] + 0.5 < self.zone[hub_to]:
                return self.zone[actual_hub] + 0.5
        elif hub_to.zone_type == ZoneType.RESTRICTED:
            if self.zone[actual_hub] + 2 < self.zone[hub_to]:
                return self.zone[actual_hub] + 2
        return

    def get_full_path(self) -> list:
        """Reconstruct the full path by walking back through the parents.

        Returns:
            list: The full path from the start hub to the end hub.
        """
        for hubs in self.path.keys():
            hub = hubs
            path = [hub]
        if len(self.path):
            while hub != self.start:
                hub = self.path[hub]
                path.append(hub)
            if self.end in path:
                self.path_found = True
            return list(reversed(path))
        else:
            return [self.start]

    def get_lowest_hub(self) -> Any:
        """Find the unprocessed hub with the lowest current cost.

        Returns:
            Hub: The hub with the smallest current cost.
        """
        lowest_cost = min([v for k, v in self.zone.items()])
        r_dict = {v: k for k, v in self.zone.items()}
        return r_dict[lowest_cost]
