import pygame as pg
import math

# from map import world_map
# from config import *
# from player_settings import *
from player_control import Player
from ray_casting import ray_casting
from draw import Drawing
from sprites_log import *


pg.init()

pg.mouse.set_visible(False)

# Инициализация часов и экрана
Screen = pg.display.set_mode((WIDTH, HEIGHT))
mini_map_screen = pg.Surface(MINIMAP_RESOLUTION)
clock = pg.time.Clock()

# Инициализация объектов класса спрайт
sprites = Sprites()

# Инициализация игрока
player = Player(sprites)
drawing = Drawing(Screen, mini_map_screen, player)

if __name__ == '__main__':
    while 1:
        # Проверка событий
        for event in pg.event.get():
            # Проверка на закрытие окна
            if event.type == pg.QUIT:
                exit()

        # Движение персоонажа
        player.to_move()

        # Заливка экрана
        Screen.fill(colors["black"])

        drawing.draw_background(player.angle)

        walls = ray_casting(player, drawing.textures)

        drawing.draw_map(walls + [obj.obj_detector(player) for obj in sprites.obj_list])

        # Отрисовка счётчика показателей
        drawing.fps_rate(clock)
        drawing.pos(player)
        drawing.player_weapon()

        # стрельба
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and not player.shot:
                    player.shot = True

        # Отрисовка мини-карты
        # drawing.draw_mini_map(player)

        pg.display.flip()

        # Установка количества кадров в секунду
        clock.tick(FPS)
        # clock.tick()

# =================     ===============     ===============   ========  ========
# \\ . . . . . . .\\   //. . . . . . .\\   //. . . . . . .\\  \\. . .\\// . . //
# ||. . ._____. . .|| ||. . ._____. . .|| ||. . ._____. . .|| || . . .\/ . . .||
# || . .||   ||. . || || . .||   ||. . || || . .||   ||. . || ||. . . . . . . ||
# ||. . ||   || . .|| ||. . ||   || . .|| ||. . ||   || . .|| || . | . . . . .||
# || . .||   ||. _-|| ||-_ .||   ||. . || || . .||   ||. _-|| ||-_.|\ . . . . ||
# ||. . ||   ||-'  || ||  `-||   || . .|| ||. . ||   ||-'  || ||  `|\_ . .|. .||
# || . _||   ||    || ||    ||   ||_ . || || . _||   ||    || ||   |\ `-_/| . ||
# ||_-' ||  .|/    || ||    \|.  || `-_|| ||_-' ||  .|/    || ||   | \  / |-_.||
# ||    ||_-'      || ||      `-_||    || ||    ||_-'      || ||   | \  / |  `||
# ||    `'         || ||         `'    || ||    `'         || ||   | \  / |   ||
# ||            .===' `===.         .==='.`===.         .===' /==. |  \/  |   ||
# ||         .=='   \_|-_ `===. .==='   _|_   `===. .===' _-|/   `==  \/  |   ||
# ||      .=='    _-'    `-_  `='    _-'   `-_    `='  _-'   `-_  /|  \/  |   ||
# ||   .=='    _-'          `-__\._-'         `-_./__-'         `' |. /|  |   ||
# ||.=='    _-'                                                     `' |  /==.||
# =='    _-'                                                            \/   `==
# \   _-'                                                                `-_
