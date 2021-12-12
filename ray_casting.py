import pygame as pg
from config import *
from map import world_map


def select_cur_sector(x, y):
    return (x // TILE_WIDTH) * TILE_WIDTH, (y // TILE_WIDTH) * TILE_WIDTH


def ray_casting(sc, player_pos, player_angle, textures):
    cur_angle = player_angle - HALF_FOV
    s_X, s_Y = player_pos
    c_X, c_Y = select_cur_sector(s_X, s_Y)
    for ray in range(NUM_OF_RAYS):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)

        # Поиск пересечений с границами квадрантов
        x, dx = (c_X + TILE_WIDTH, 1) if cos_a >= 0 else (c_X, -1)
        for i in range(0, WIDTH, TILE_WIDTH):
            depth_v = (x - s_X) / cos_a
            yv = s_Y + depth_v * sin_a
            tile_v = select_cur_sector(x + dx, yv)
            if tile_v in world_map:
                texture_v = world_map[tile_v]
                break
            x += dx * TILE_WIDTH

        y, dy = (c_Y + TILE_WIDTH, 1) if sin_a >= 0 else (c_Y, -1)
        for i in range(0, WIDTH, TILE_WIDTH):
            depth_h = (y - s_Y) / sin_a
            xh = s_X + depth_h * cos_a
            tile_h = select_cur_sector(xh, y + dy)
            if tile_h in world_map:
                texture_h = world_map[tile_h]
                break
            y += dy * TILE_WIDTH

        # Отображение ближайшего пересечения
        depth, offset, cur_texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
        offset = int(offset) % TILE_WIDTH
        depth *= math.cos(player_angle - cur_angle)
        depth = max(depth, 0.00001)
        projection_height = min(int(PROJECTION_C / depth), 2 * HEIGHT)

        wall_texture = textures[cur_texture].subsurface(offset * T_Scale, 0, T_Scale, T_HEIGHT)
        wall_texture = pg.transform.scale(wall_texture, (SCALE, projection_height))
        sc.blit(wall_texture, (ray * SCALE, HALF_HEIGHT - projection_height // 2))

        cur_angle += dt_ANGLE