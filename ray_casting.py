import pygame as pg
from config import *
from map import wrold_map


def ray_casting(sc, player_pos, player_angle):
    cur_angle = player_angle - HALF_FOV
    s_X, s_Y = player_pos
    for ray in range(NUM_OF_RAYS):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)
        for depth in range(len_of_rays):
            x = s_X + depth * cos_a
            y = s_Y + depth * sin_a
            if (x // TILE_WIDTH * TILE_WIDTH, y // TILE_WIDTH * TILE_WIDTH) in wrold_map:
                depth *= math.cos(player_angle - cur_angle)
                projection_height = PROJECTION_C / depth
                dt_color = 255 / (1 + depth ** 2 * 0.0001)
                pg.draw.rect(sc, (dt_color, dt_color, dt_color), (ray * SCALE, HALF_HEIGHT - projection_height // 2,
                                                   SCALE, projection_height))
                break
        cur_angle += dt_ANGLE