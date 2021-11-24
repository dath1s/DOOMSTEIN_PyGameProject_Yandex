import pygame as pg
import math

from map import wrold_map
from config import *
from player_settings import *
from player_control import Player
from ray_casting import ray_casting


pg.init()

# Инициализация часов и экрана
Screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

# Инициализация игрока
player = Player()

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

        # Отрисовка неба и пола
        pg.draw.rect(Screen, colors["light-blue"], (0, 0, WIDTH, HALF_HEIGHT))
        pg.draw.rect(Screen, colors["dark-gray"], (0, HALF_HEIGHT, WIDTH, HEIGHT))

        ray_casting(Screen, player.get_pos, player.angle)

        pg.display.flip()
        # Установка количества кадров в секунду
        clock.tick(FPS)