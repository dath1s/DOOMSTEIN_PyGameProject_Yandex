import pygame as pg
import math

from map import world_map
from config import *
from player_settings import *
from player_control import Player
from ray_casting import ray_casting
from draw import Drawing
from sprites_log import *


pg.init()

# Инициализация часов и экрана
Screen = pg.display.set_mode((WIDTH, HEIGHT))
mini_map_screen = pg.Surface((400, 160))
clock = pg.time.Clock()

# Инициализация игрока
player = Player()
drawing = Drawing(Screen, mini_map_screen)

# Инициализация оюъектов класса спрайт
sprites = Sprites()


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

        drawing.draw_map(walls + [obj.obj_detector(player, walls) for obj in sprites.obj_list])

        # Отрисовка счётчика fps
        drawing.fps_rate(clock)

        # Отрисовка мини-карты
        drawing.draw_mini_map(player)

        pg.display.flip()

        # Установка количества кадров в секунду
        clock.tick(FPS)
        # clock.tick()
