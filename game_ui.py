# py_game.py
import sys
import pygame
# from py_game import K_LEFT
from fly_in import Map
import operator

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
PURPLE = (153, 51, 255)
BROWN = (165, 82, 0)
ORANGE = (255, 165, 0)
MAROON = (128, 0, 0)
GOLD = (255, 215, 0)
DARKRED = (139, 0, 0)
VIOLET = (215, 95, 215)
CRIMSON = (220, 20, 60)
LIME = (50, 205, 50)
RAINBOW = (255, 0, 0)


class GameUI:
    def __init__(self, my_map: Map):
        pygame.init()
        self.my_map = my_map
        self.screen = pygame.display.set_mode((1500, 1200))
        pygame.display.set_caption("Fly In")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        self.step_delay_ms = 1000
        self.last_step = 0
        self.cam_pos = [0, 0]

        self.points = self._build_points()

    def _build_points(self):
        # Simple scaling from map coordinates to screen coordinates
        xs = [hub.position[0] for hub in self.my_map.hubs]
        ys = [hub.position[1] for hub in self.my_map.hubs]
        min_x, _ = min(xs), max(xs)
        min_y, _ = min(ys), max(ys)

        def convert(pos):
            x, y = pos
            sx = 60 + (x - min_x) * 100
            sy = 60 + (y - min_y) * 100
            return sx, sy
        # tuple(map(operator.add, hub.position, self.cam_pos))
        return {
            hub.id: convert(
                tuple(map(operator.add, list(hub.position),
                          self.cam_pos))) for hub in self.my_map.hubs
                }

    def draw(self, i: int):
        self.screen.fill(WHITE)

        move_heading = self.font.render(f"Move number {i}", True, BLACK)
        self.screen.blit(move_heading, (0, 0))
        # Draw connections first
        for connection in self.my_map.connections:
            a, b = connection.linked_members
            if a and b:
                pygame.draw.line(
                    self.screen,
                    BLACK,
                    self.points[a.id],
                    self.points[b.id],
                    2)

        # Draw hubs
        for hub in self.my_map.hubs:
            pos = self.points[hub.id]
            color = RED if hub == self.my_map.start_hub\
                else BLUE if hub == self.my_map.end_hub else BLACK

            pygame.draw.circle(self.screen, color, pos, 15)
            label = self.font.render(hub.id, True, BLACK)
            self.screen.blit(label, (pos[0] + 15, pos[1] + 15))

            # Draw drones on top of the hub
            for i, drone in enumerate(
                    hub.drones + [h[0] for h in hub.waiting_drones]):
                pygame.draw.circle(self.screen,
                                   BLUE,
                                   (pos[0], pos[1] + 25 + i * 15),
                                   6,
                                   draw_top_right=True,
                                   draw_top_left=True,
                                   draw_bottom_left=True,
                                   draw_bottom_right=True)
                if hub.zone == "RESTRICTED":
                    to_print = drone.id + "(waiting)"
                else:
                    to_print = drone.id
                d_label = self.font.render(to_print, True, BLACK)
                self.screen.blit(d_label, (pos[0] + 5, pos[1] + 25 + i * 15))

        pygame.display.flip()

    def run(self):
        running = True
        i = 0
        while running:

            now = pygame.time.get_ticks()
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                self.cam_pos[0] += 0.1
                self.points = self._build_points()
                # move to the left, decrement x
            elif key[pygame.K_RIGHT]:
                # increment x
                self.cam_pos[0] -= 0.1
                self.points = self._build_points()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Advance simulation on a timer
            if now - self.last_step >= self.step_delay_ms:
                running = self.my_map.make_move()
                i += 1
                print("\b\b")
                self.last_step = now

            self.draw(i - 1)
            self.clock.tick(160)

        print("Total moves: ", i - 1)
        pygame.quit()
        sys.exit()
