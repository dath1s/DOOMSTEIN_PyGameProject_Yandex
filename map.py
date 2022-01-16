from config import *
import pygame as pg
# from numba.core import types
# from numba.typed import Dict
# from numba import int32


_ = False
map = \
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1, 1],
        [1, 1, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, 1, 1, 1, _, _, _, _, 1, 1],
        [1, 1, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, 2, _, _, _, _, 1, 1],
        [1, 1, _, _, 2, 1, _, _, _, 1, 1, 1, _, 1, 1, _, _, _, _, 2, _, _, _, _, 1, 1],
        [1, 1, _, _, 1, 1, _, _, 1, 1, _, _, _, _, 1, 1, _, _, _, 2, 2, _, _, _, 1, 1],
        [1, 1, _, _, 1, _, _, _, 1, _, _, _, _, _, _, 1, _, _, _, _, 1, _, _, _, 1, 1],
        [1, 1, _, _, 1, _, _, _, _, _, _, 2, 2, _, _, _, _, _, _, _, _, _, _, _, 1, 1],
        [1, 1, _, _, 2, _, _, _, 1, _, _, 2, 2, _, _, 1, _, _, _, _, _, _, _, _, 1, 1],
        [1, 1, _, _, _, _, _, _, 1, _, _, _, _, _, _, 1, _, _, _, _, _, _, _, _, 1, 1],
        [1, 1, _, _, _, _, _, _, 1, 1, _, _, _, _, 1, 1, _, _, _, 1, 1, 2, _, _, 1, 1],
        [1, 1, _, _, _, _, _, _, _, 1, 1, _, 1, 1, 1, _, _, _, _, 1, 1, 1, _, _, 1, 1],
        [1, 1, _, _, 1, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, 1, 1, 1, _, _, 1, 1],
        [1, 1, _, _, 2, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, 1, 1, 1, _, _, 1, 1],
        [1, 1, _, _, 2, _, _, _, _, _, _, 2, 2, _, _, _, _, _, _, 2, 1, 1, _, _, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]

WORLD_WIDTH = len(map[0]) * TILE_WIDTH
WORLD_HEIGHT = len(map) * TILE_WIDTH

# world_map = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)
world_map = {}
mini_map = set()

walls_collision = []

for num, row in enumerate(map):
    for elem_num, char in enumerate(row):
        if char:
            mini_map.add((elem_num * MAP_TILE, num * MAP_TILE))
            walls_collision.append(pg.Rect(elem_num * TILE_WIDTH,
                                           num * TILE_WIDTH,
                                           TILE_WIDTH, TILE_WIDTH))

            if char == 1:
                world_map[(elem_num * TILE_WIDTH, num * TILE_WIDTH)] = 1
            elif char == 2:
                world_map[(elem_num * TILE_WIDTH, num * TILE_WIDTH)] = 2
