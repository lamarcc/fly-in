from parser.errors import Colors

class PathfindingError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        error_type = Colors.FAIL + Colors.BOLD + "[PathfindingError] " + Colors.ENDC + Colors.BOLD
        return error_type + self.message + Colors.ENDC


class Pathfinding():
    def __init__(self, map):
        self.start = map.start_hub
        self.end = map.end_hub
        self.path = {}
        self.zone = {}
        self.path_found = False
        for hub in map.hubs.values():
            if hub.zone_type == "blocked":
                continue
            if hub == self.start:
                self.zone[self.start] = 0
            else:
                self.zone[hub] = float('inf')

    def find_path(self):
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
        full_path = self.get_full_path()
        if self.path_found == False:
            raise PathfindingError("No valid path found")
        return full_path

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
        for hubs in self.path.keys():
            hub = hubs
            path = [hub]
        full_path = []
        if len(self.path):
            while hub != self.start:
                hub = self.path[hub]
                path.append(hub)
            for i in reversed(path):
                full_path.append(i)
            if self.end in full_path:
                self.path_found = True
            return full_path
        else:
            return [self.start]

    def get_lowest_hub(self):
        lowest_cost = min([v for k, v in self.zone.items()])
        r_dict = {v: k for k, v in self.zone.items()}
        return r_dict[lowest_cost]
