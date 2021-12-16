from player_settings import *
import pygame as pg
import math
from config import *


class Player:
    def __init__(self):
        self.pos = self.x, self.y = player_start_pos
        self.angle = player_view_angle
        self.sense = 0.001

    @property
    def get_pos(self):
        return int(self.x), int(self.y)

    def to_move(self):
        self.to_move_mouse()
        self.to_move_keys()

    def to_move_mouse(self):
        if pg.mouse.get_focused():
            dt = pg.mouse.get_pos()[0] - HALF_WIDTH
            pg.mouse.set_pos((HALF_WIDTH, HALF_HEIGHT))
            self.angle += dt * self.sense

    def to_move_keys(self):
        keys = pg.key.get_pressed()
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        # Проверка на нажатия
        if keys[pg.K_ESCAPE]:
            exit()
        if keys[pg.K_w]:
            self.x += player_speed * cos_a
            self.y += player_speed * sin_a
        if keys[pg.K_s]:
            self.x += -player_speed * cos_a
            self.y += -player_speed * sin_a
        if keys[pg.K_d]:
            self.x += -player_speed * sin_a
            self.y += player_speed * cos_a
        if keys[pg.K_a]:
            self.x += player_speed * sin_a
            self.y += -player_speed * cos_a
        if keys[pg.K_LEFT]:
            self.angle -= 0.02
        if keys[pg.K_RIGHT]:
            self.angle += 0.02

        self.angle %= DOUBLE_PI