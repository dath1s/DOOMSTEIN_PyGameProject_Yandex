import pygame as pg
from config import *
from collections import deque


class Sprites:
    def __init__(self):
        self.sprite_params = {
            'sprite_barrel':{
                'sprite': pg.image.load('sprites/barrel/base/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 1.8,
                'scale': 0.4,
                'animation': deque([
                    pg.image.load(f'sprites/barrel/anim/{i}.png').convert_alpha() for i in range(8)
                ]),
                'animation_dist': 800,
                'animation_speed': 10,
                'blocked': True
            },
            'sprite_devil': {
                'sprite': [pg.image.load(f'sprites/devil/base/{i}.png').convert_alpha() for i in range(8)],
                'viewing_angles': True,
                'shift': -0.2,
                'scale': 1.1,
                'animation': deque(
                    [pg.image.load(f'sprites/devil/anim/{i}.png').convert_alpha() for i in range(9)]),
                'animation_dist': 150,
                'animation_speed': 10,
                'blocked': True
            },
            'sprite_flame': {
                'sprite': pg.image.load('sprites/flame/base/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.7,
                'scale': 0.6,
                'animation': deque(
                    [pg.image.load(f'sprites/flame/anim/{i}.png').convert_alpha() for i in range(16)]),
                'animation_dist': 800,
                'animation_speed': 5,
                'blocked': False
            }
        }
        # self.sprite_types = {
        #     'barrel': pg.image.load('sprites/barrel/0.png').convert_alpha(),
        #     'devil': [pg.image.load(f'sprites/Devil/{i}.png').convert_alpha() for i in range(8)]
        # }

        self.obj_list = \
            [
                SpriteObj(self.sprite_params['sprite_barrel'], (7.1, 2.8)),
                SpriteObj(self.sprite_params['sprite_barrel'], (5.9, 2.8)),
                SpriteObj(self.sprite_params['sprite_devil'], (8.7, 2.8)),
                SpriteObj(self.sprite_params['sprite_flame'], (10.5, 2.8))
            ]

    @property
    def sprite_shot(self):
        return min([obj.is_on_fireway for obj in self.obj_list], default=(float('inf'), 0))

class SpriteObj:
    def __init__(self, params, pos):
        self.obj = params['sprite']
        self.viewing_angles = params['viewing_angles']
        self.x, self.y = pos[0] * TILE_WIDTH, pos[1] * TILE_WIDTH
        self.shift = params['shift']
        self.scale = params['scale']
        self.animation = params['animation']
        self.animation_dist = params['animation_dist']
        self.animation_speed = params['animation_speed']
        self.animation_counter = 0
        self.blocked = params['blocked']
        self.side = 30

        if self.viewing_angles:
            self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.obj)}

    @property
    def is_on_fireway(self):
        if Center_RAY - self.side // 2 < self.cur_ray < Center_RAY + self.side // 2 and self.blocked:
            return self.dist_to_sprite, self.proj_height
        return float('inf'), None

    @property
    def pos(self):
        return self.x - self.side // 2, self.y - self.side // 2

    def obj_detector(self, player):
        dx, dy = self.x - player.x, self.y - player.y
        self.dist_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        self.theta = math.atan2(dy, dx)
        gamma = self.theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += DOUBLE_PI

        dt_rays = int(gamma / dt_ANGLE)
        self.cur_ray = Center_RAY + dt_rays
        self.dist_to_sprite *= math.cos(HALF_FOV - self.cur_ray * dt_ANGLE)

        fake_ray = self.cur_ray + NONE_VISIABLE_RAYS

        if 0 <= fake_ray <= FAKE_RAYS_RANGE and self.dist_to_sprite > 30:
            self.proj_height = min(int(PROJECTION_C / self.dist_to_sprite * self.scale), DOUBLE_HEIGHT)
            half_projection_height = self.proj_height // 2
            shift = half_projection_height * self.shift

            if self.viewing_angles:
                if self.theta < 0:
                    self.theta += DOUBLE_PI
                self.theta = 360 - int(math.degrees(self.theta))

                for angles in self.sprite_angles:
                    if self.theta in angles:
                        self.obj = self.sprite_positions[angles]

            # Анимация спрайтов
            sprite_obj = self.obj
            if self.animation and self.dist_to_sprite < self.animation_dist:
                sprite_obj = self.animation[0]
                if self.animation_counter < self.animation_speed:
                    self.animation_counter += 1
                else:
                    self.animation.rotate()
                    self.animation_counter = 0

            # Проекция спрайта
            sprite_position = (self.cur_ray * SCALE - half_projection_height, HALF_HEIGHT - half_projection_height + shift)
            sprite = pg.transform.scale(sprite_obj, (self.proj_height, self.proj_height))

            return (self.dist_to_sprite, sprite, sprite_position, None)
        else:
            return (False,)