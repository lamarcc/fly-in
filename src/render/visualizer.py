from engine import Hub, Connection, Drone
import pygame
import time

class Color():
    rgb = {
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

class Visualizer():
    def __init__(self, map, simulation):
        self.map = map
        self.simulation = simulation

    def create_window(self, movement_history):
        self.all_coordinate = [(pos.pos_x, pos.pos_y) for pos in self.map.hubs.values()]
        self.max_x = max(x for x, y in self.all_coordinate)
        self.min_x = min(x for x, y in self.all_coordinate)
        self.max_y = max(y for x, y in self.all_coordinate)
        self.min_y = min(y for x, y in self.all_coordinate)
        self.zones = [zone for zone in self.map.hubs.values()]
        self.hub_r = 50
        self.min_spacing = 50
        self.margin = 100
        self.scale = (2 * self.hub_r + self.min_spacing) / 0.8
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
        show_text = font.render(text, True, Color.rgb['white'])
        self.screen.blit(show_text, pos)

    def print_info(self):
        self.print_text(f'{self.idx} / {self.lapmax - 1}', 60, (20, 20))
        self.print_text("Escape: Close window", 20, (20, self.height - 70))
        self.print_text("Left-Right Arrow: Previous/Next Image", 20, (20, self.height - 50))
        self.print_text("Down-Up Arrow: Previous/Next Fast play", 20, (20, self.height - 30))

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
            pygame.draw.circle(self.background, Color.rgb[hub.color], (pos_x, pos_y), self.hub_r)
            name = self.contract_name(hub.name)
            hub_name = h_text.render(name, True, (255, 255, 255))
            shadow = h_text.render(name, True, Color.rgb['black'])
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
            pygame.draw.line(self.background, (100, 100, 100), (x1, y1), (x2, y2), 5)

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
                    pygame.draw.line(img, (255, 255, 255), (x1, y1), (x2, y2), 5)
                else:
                    pos_x, pos_y = self.pixel_pos(d_pos.pos_x, d_pos.pos_y)
                    pygame.draw.circle(img, (150, 150, 150), (pos_x, pos_y + 7), 10)
                    pygame.draw.circle(img, (230, 230, 230), (pos_x, pos_y + 7), 8)
                    text = d_text.render(str(d_number), True, Color.rgb['black'])
                    pos = text.get_rect(center=(pos_x, pos_y + 7))
                    img.blit(text, pos)
            i += 1
