from player_settings import *
from config import *
import pygame as pg
from map import walls_collision


class Player:
    def __init__(self, sprites):
        self.pos = self.x, self.y = player_start_pos
        self.sprites = sprites
        self.angle = player_view_angle
        self.sense = 0.001
        # Коллизии
        self.side = 50
        self.rect = pg.Rect(*player_start_pos, self.side, self.side)
        self.shot = False
        self.health = 100
        self.score = 0

    @property
    def get_pos(self):
        return int(self.x), int(self.y)

    @property
    def list_of_collisions(self):
        return walls_collision + [
            pg.Rect(*obj.pos, obj.side, obj.side) for obj in self.sprites.obj_list if obj.blocked
        ]

    def get_cur_pos(self):
        return round(self.x / TILE_WIDTH, 2), round(self.y / TILE_WIDTH, 2)

    def detection_of_walls(self, dx, dy):
        next_rect = self.rect.copy()
        next_rect.move_ip(dx, dy)
        hit_indexes = next_rect.collidelistall(self.list_of_collisions)

        if len(hit_indexes):
            dt_x, dt_y = 0, 0
            for hit_index in hit_indexes:
                hit_rect = self.list_of_collisions[hit_index]
                if dx > 0:
                    dt_x += next_rect.right - hit_rect.left
                else:
                    dt_x += hit_rect.right - next_rect.left

                if dy > 0:
                    dt_y += next_rect.bottom - hit_rect.top
                else:
                    dt_y += hit_rect.bottom - next_rect.top

            if abs(dt_x - dt_y) < 10:
                dx, dy = 0, 0
            elif dt_x > dt_y:
                dy = 0
            elif dt_y > dt_x:
                dx = 0
        self.x += dx
        self.y += dy

    def to_move(self):
        self.to_move_mouse()
        self.to_move_keys()

        self.rect.center = self.x, self.y
        self.angle %= DOUBLE_PI

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
            dx = player_speed * cos_a
            dy = player_speed * sin_a
            self.detection_of_walls(dx, dy)
        if keys[pg.K_s]:
            dx = -player_speed * cos_a
            dy = -player_speed * sin_a
            self.detection_of_walls(dx, dy)
        if keys[pg.K_d]:
            dx = -player_speed * sin_a
            dy = player_speed * cos_a
            self.detection_of_walls(dx, dy)
        if keys[pg.K_a]:
            dx = player_speed * sin_a
            dy = -player_speed * cos_a
            self.detection_of_walls(dx, dy)

        if keys[pg.K_LEFT]:
            self.angle -= 0.02
        if keys[pg.K_RIGHT]:
            self.angle += 0.02

        if keys[pg.K_f]:
            if not self.shot:
                self.shot = True
