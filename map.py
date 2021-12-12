from config import *

map = \
    [
        "111111111111",
        "1..........1",
        "1..22...1111",
        "1..22......1",
        "1.......2..1",
        "1..1...222.1",
        "1..2.......1",
        "111111111111"
    ]

world_map = {}
mini_map = set()
for num, row in enumerate(map):
    for elem_num, char in enumerate(row):
        if char != ".":
            mini_map.add((elem_num * MAP_TILE, num * MAP_TILE))

            if char == '1':
                world_map[(elem_num * TILE_WIDTH, num * TILE_WIDTH)] = "1"
            elif char == '2':
                world_map[(elem_num * TILE_WIDTH, num * TILE_WIDTH)] = "2"
