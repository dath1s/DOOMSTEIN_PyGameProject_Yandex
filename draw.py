import pygame as pg
from config import *
from ray_casting import ray_casting
from map import mini_map


class Drawing:
    def __init__(self, sc, mini_map_surf):
        self.sc = sc
        self.mini_map_surf = mini_map_surf
        self.font = pg.font.SysFont('Arial', 48, bold=True)

    def draw_background(self):
        # Отрисовка неба и пола
        pg.draw.rect(self.sc, colors["light-blue"], (0, 0, WIDTH, HALF_HEIGHT))
        pg.draw.rect(self.sc, colors["light-gray"], (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def draw_map(self, player_pos, player_angle):
        ray_casting(self.sc, player_pos, player_angle)

    def fps_rate(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, False, colors["green"])
        self.sc.blit(render, (20, 20))

    def draw_mini_map(self, player):
        self.mini_map_surf.fill(colors["black"])
        player_x, player_y = player.x // MAP_SCALE, player.y // MAP_SCALE
        pg.draw.line(self.mini_map_surf, colors["green"], (player_x, player_y),
                     (player_x + 20 * math.cos(player.angle),
                      player_y + 20 * math.sin(player.angle)), 5)
        for x, y in mini_map:
            pg.draw.rect(self.mini_map_surf, (1, 50, 32), (x, y, TILE_WIDTH // MAP_SCALE, TILE_WIDTH // MAP_SCALE))
        pg.draw.circle(self.mini_map_surf, colors["yellow"], (int(player_x), player_y), 5)
        self.sc.blit(self.mini_map_surf, (WIDTH - WIDTH // MAP_SCALE, 0))