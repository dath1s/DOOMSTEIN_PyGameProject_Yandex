from config import *

map = \
    [
        "WWWWWWWWWWWW",
        "W..........W",
        "W..WW...WWWW",
        "W..WW......W",
        "W.......W..W",
        "W..W...WWW.W",
        "W..W.......W",
        "WWWWWWWWWWWW"
    ]

world_map = set()
mini_map = set()
for num, row in enumerate(map):
    for elem_num, char in enumerate(row):
        if char == "W":
            world_map.add((elem_num * TILE_WIDTH, num * TILE_WIDTH))
            mini_map.add((elem_num * MAP_TILE, num * MAP_TILE))