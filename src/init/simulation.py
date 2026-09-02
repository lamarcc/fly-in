from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Tuple, Any
from .parsing import Parse
from enum import Enum
import pygame
import time


class Simulation():
    def __init__(self):
        self.map = Map()
        self.parse = Parse()
        self.visualizer = Visualizer(self.map, self)
        self.is_running = False
        self.drones = []
        self.drones_finished = []
        self.drones_pos = {}

    def init_drones(self, road):
        for i in range(1, self.map.nb_drones + 1):
            drone = Drone(i, self.map, road)
            self.drones.append(drone)

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
            hub_a = self.map.hubs[info['hub_a']]
            hub_b = self.map.hubs[info['hub_b']]
            name = f'{hub_a.name}-{hub_b.name}'
            connection = Connection(name, hub_a, hub_b, info["metadata"])
            self.map.connections[name] = connection
        for connection in self.map.connections.values():
            connection.hub_a.connected_to.append(connection.hub_b)
            connection.hub_b.connected_to.append(connection.hub_a)

    def init(self):
        self.map.nb_drones = self.parse.nb_drones
        self.init_hubs(self.parse.hubs)
        self.init_connections(self.parse.connection)

    def run(self):
        p = Pathfinding(self.map)
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
                drone.go_to()
                if drone.pos == self.map.end_hub:
                    self.drones_finished.append(drone)
            lap += 1
            self.drones_pos[f'Lap{lap}'] = {drone.number: drone.pos for drone in self.drones}
        self.visualizer.create_window(self.drones_pos)


class Map():
    def __init__(self):
        self.map = []
        self.nb_drones = 0
        self.start_hub = None
        self.end_hub = None
        self.hubs = {}
        self.connections = {}


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

    def get_pos(self):
        return (self.pos_x, self.pos_y)

    def check_capacity(self):
        if self.occupied + 1 <= self.max_capacity:
            return True
        else:
            return False


class Connection():
    def __init__(self, name, hub_a: Hub, hub_b: Hub, data: dict):
        self.name = name
        self.hub_a = hub_a
        self.hub_b = hub_b
        self.max_capacity = data["max_link_capacity"]
        self.occupied = 0
        self.passed = 0

    def check_capacity(self):
        if self.occupied + 1 <= self.max_capacity:
            return True
        else:
            return False


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
        self.path = list(road)

    def go_to(self):
        if self.pos == self.map.end_hub:
            return
        next_move = self.path[1]
        if isinstance(self.pos, Hub) and next_move.zone_type == "restricted":
            for name in self.map.connections.keys():
                if self.pos.name in name and next_move.name in name:
                    connection = self.map.connections[name]
                    if not connection.check_capacity():
                        self.count += 1
                        return
                    self.pos.occupied -= 1
                    self.pos = connection
                    connection.passed += 1
                    self.pos.occupied += 1
                    self.count += 1
                    return
        if isinstance(self.pos, Connection):
            if not next_move.check_capacity():
                self.count += 1
                return
            self.pos.occupied -= 1
            self.pos = next_move
            self.pos.occupied += 1
            self.path.pop(1)
            return
        if not next_move.check_capacity():
            self.count += 1
            return
        for name in self.map.connections.keys():
            if self.pos.name in name and next_move.name in name:
                connection = self.map.connections[name]
                if connection.passed >= connection.max_capacity:
                    self.count += 1
                    return
        connection.passed += 1
        self.pos.occupied -= 1
        self.pos = next_move
        self.pos.occupied += 1
        self.path.pop(1)
        self.count += 1


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


class Visualizer():
    def __init__(self, map, simulation):
        self.map = map
        self.simulation = simulation
        self.color = {
                "none": (200, 200, 200),
                "red": (255, 0, 0),
                "green": (0, 128, 0),
                "blue": (0, 0, 255),
                "yellow": (255, 255, 0),
                "orange": (255, 165, 0),
                "purple": (128, 0, 128),
                "pink": (255, 192, 203),
                "brown": (139, 69, 19),
                "black": (0, 0, 0),
                "white": (255, 255, 255),
                "gray": (128, 128, 128),
                "cyan": (0, 255, 255),
                "magenta": (255, 0, 255),
                "lime": (0, 255, 0),
                "navy": (0, 0, 128),
                "teal": (0, 128, 128),
                "maroon": (128, 0, 0),
                "gold": (255, 215, 0),
                "darkred": (139, 0, 0),
                "violet": (238, 130, 238),
                "crimson": (220, 20, 60),
                "rainbow": (255, 105, 180),
        }

    def create_window(self, movement_history):
        self.all_coordinate = [(pos.pos_x, pos.pos_y) for pos in self.map.hubs.values()]
        self.max_x = max(x for x, y in self.all_coordinate)
        self.min_x = min(x for x, y in self.all_coordinate)
        self.max_y = max(y for x, y in self.all_coordinate)
        self.min_y = min(y for x, y in self.all_coordinate)
        self.zones = [zone for zone in self.map.hubs.values()]
        self.hub_r = 10
        self.min_spacing = 40
        self.margin = 100
        self.scale = (2 * self.hub_r + self.min_spacing) / 1
        self.width = (self.max_x - self.min_x) * self.scale + 2 * self.margin
        self.height = (self.max_y - self.min_y) * self.scale + 2 * self.margin
        self.image = []

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Fly-in")

        pygame.font.init()

        self.lapmax = len(movement_history.keys())
        for i in range(self.lapmax):
            img = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            self.image.append(img)

        self.background = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.screen.fill((30, 30, 30))
        self.draw_map()
        self.draw_drones(movement_history)

        self.idx = 0
        self.build_image()
        running = True
        while running:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_UP]:
                self.idx += 1
                if self.idx >= self.lapmax:
                    self.idx = self.lapmax - 1
                self.build_image()
                time.sleep(0.1)
            if pressed[pygame.K_DOWN]:
                self.idx -= 1
                if self.idx <= 0:
                    self.idx = 0
                self.build_image()
                time.sleep(0.1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_RIGHT:
                        self.idx += 1
                        if self.idx >= self.lapmax:
                            self.idx = self.lapmax - 1
                        self.build_image()
                    if event.key == pygame.K_LEFT:
                        if self.idx <= 0:
                            continue
                        self.idx -= 1
                        self.build_image()
            pygame.display.flip()

    def print_text(self, text, size, pos):
        font = pygame.font.SysFont(None, size)
        show_text = font.render(text, True, self.color['white'])
        self.screen.blit(show_text, pos)

    def print_info(self):
        self.print_text(f'{self.idx} / {self.lapmax - 1}', 30, (20, 20))
        self.print_text("Escape: Close window", 20, (20, self.height - 70))
        self.print_text("Left-Right: Previous/Next Image", 20, (20, self.height - 50))
        self.print_text("Up-Down: Previous/Next Fast play", 20, (20, self.height - 30))

    def build_image(self):
        self.screen.fill((30, 30, 30))
        self.print_info()
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.image[self.idx], (0, 0))

    def pixel_pos(self, x, y):
        if self.max_x == self.min_x:
            pos_x = self.width / 2
        else:
            pos_x = self.margin + (x - self.min_x) / (self.max_x - self.min_x) * (self.width - 2 * self.margin)
        if self.max_y == self.min_y:
            pos_y = self.height / 2
        else:
            pos_y = self.margin + (y - self.min_y) / (self.max_y - self.min_y) * (self.height - 2 * self.margin)
        return pos_x, pos_y

    def contract_name(self, name):
        if len(name) > 2:
            character = list(name[0])
            number = [i for i in name if i.isdigit()]
        return ''.join(character+number).upper()

    def draw_hub(self):
        h_text = pygame.font.SysFont(None, 16)
        for hub in self.map.hubs.values():
            pos_x, pos_y = self.pixel_pos(hub.pos_x, hub.pos_y)
            pygame.draw.circle(self.background, self.color[hub.color], (pos_x, pos_y), 25)
            name = self.contract_name(hub.name)
            hub_name = h_text.render(name, True, (255, 255, 255))
            shadow = h_text.render(name, True, self.color['black'])
            text_pos = hub_name.get_rect(center=(pos_x, pos_y - 12))
            shadow_pos = shadow.get_rect(center=(pos_x + 1, pos_y - 10))
            self.background.blit(shadow, shadow_pos)
            self.background.blit(hub_name, text_pos)

    def draw_connection(self):
        for connection in self.map.connections.values():
            x, y = connection.hub_a.get_pos()
            x1, y1 = self.pixel_pos(x, y)
            x, y = connection.hub_b.get_pos()
            x2, y2 = self.pixel_pos(x, y)
            pygame.draw.line(self.background, (100, 100, 100), (x1, y1), (x2, y2), 2)

    def draw_map(self):
        self.draw_connection()
        self.draw_hub()

    def draw_drones(self, lap_history):
        i = 0
        d_text = pygame.font.SysFont(None, 16)
        for img in self.image:
            for d_number, d_pos in lap_history[f'Lap{i}'].items():
                if isinstance(d_pos, Connection):
                    a_x, a_y = d_pos.hub_a.get_pos()
                    b_x, b_y = d_pos.hub_b.get_pos()
                    x1, y1 = self.pixel_pos(a_x, a_y)
                    x2, y2 = self.pixel_pos(b_x, b_y)
                    pygame.draw.line(img, (255, 255, 255), (x1, y1), (x2, y2), 2)
                else:
                    pos_x, pos_y = self.pixel_pos(d_pos.pos_x, d_pos.pos_y)
                    pygame.draw.circle(img, (150, 150, 150), (pos_x, pos_y + 7), 10)
                    pygame.draw.circle(img, (230, 230, 230), (pos_x, pos_y + 7), 8)
                    text = d_text.render(str(d_number), True, self.color['black'])
                    pos = text.get_rect(center=(pos_x, pos_y + 7))
                    img.blit(text, pos)
            i += 1
