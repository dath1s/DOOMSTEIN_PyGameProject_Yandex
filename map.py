from config import *

map = \
    [
        "WWWWWWWWWWWW",
        "W..........W",
        "W..WW......W",
        "W..WW......W",
        "W.......W..W",
        "W..W...WWW.W",
        "W..W.......W",
        "WWWWWWWWWWWW"
    ]

wrold_map = set()
for num, row in enumerate(map):
    for elem_num, char in enumerate(row):
        if char == "W":
            wrold_map.add((elem_num * TILE_WIDTH, num * TILE_WIDTH))