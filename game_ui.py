# py_game.py
import sys
import pygame
from fly_in import Map

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
BLUE = (60, 120, 255)


class GameUI:
    def __init__(self, my_map: Map):
        pygame.init()
        self.my_map = my_map
        self.screen = pygame.display.set_mode((1800, 1200))
        pygame.display.set_caption("Fly In")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        self.step_delay_ms = 1000
        self.last_step = 0

        self.points = self._build_points()

    def _build_points(self):
        # Simple scaling from map coordinates to screen coordinates
        xs = [hub.position[0] for hub in self.my_map.hubs]
        ys = [hub.position[1] for hub in self.my_map.hubs]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        def convert(pos):
            x, y = pos
            sx = 60 + (x - min_x) * 120
            sy = 60 + (y - min_y) * 120
            return sx, sy

        return {hub.id: convert(hub.position) for hub in self.my_map.hubs}

    def draw(self):
        self.screen.fill(WHITE)

        # Draw connections first
        for connection in self.my_map.connections:
            a, b = connection.linked_members
            if a and b:
                pygame.draw.line(self.screen, BLACK, self.points[a.id], self.points[b.id], 2)
                # to_print = self.font.render((str(connection.link_cap) + " " + connection.connection), True, BLACK)
                # self.screen.blit(to_print, (pos[0] + 15, pos[1] - 10))

        # Draw hubs
        for hub in self.my_map.hubs:
            pos = self.points[hub.id]
            color = RED if hub == self.my_map.start_hub else BLUE if hub == self.my_map.end_hub else BLACK
            pygame.draw.circle(self.screen, color, pos, 15)
            label = self.font.render(hub.id, True, BLACK)
            self.screen.blit(label, (pos[0] + 15, pos[1] - 10))

            # Draw drones on top of the hub
            for i, drone in enumerate(hub.drones):
                pygame.draw.circle(self.screen,
                                   BLUE,
                                   (pos[0], pos[1] + 25 + i * 15),
                                   6,
                                   draw_top_right=True,
                                   draw_top_left=True,
                                   draw_bottom_left=True,
                                   draw_bottom_right=True)

        pygame.display.flip()

    def run(self):
        running = True
        try:
            while running:

                now = pygame.time.get_ticks()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                # Advance simulation on a timer
                if now - self.last_step >= self.step_delay_ms:
                    running = self.my_map.make_move()
                    print()
                    self.last_step = now
                self.draw()
                self.clock.tick(160)
        finally:
            pygame.quit()
            sys.exit()
