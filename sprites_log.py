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
                'animation_speed': 10
            },
            'sprite_devil': {
                'sprite': [pg.image.load(f'sprites/devil/base/{i}.png').convert_alpha() for i in range(8)],
                'viewing_angles': True,
                'shift': -0.2,
                'scale': 1.1,
                'animation': deque(
                    [pg.image.load(f'sprites/devil/anim/{i}.png').convert_alpha() for i in range(9)]),
                'animation_dist': 150,
                'animation_speed': 10
            },
            'sprite_flame': {
                'sprite': pg.image.load('sprites/flame/base/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.7,
                'scale': 0.6,
                'animation': deque(
                    [pg.image.load(f'sprites/flame/anim/{i}.png').convert_alpha() for i in range(16)]),
                'animation_dist': 800,
                'animation_speed': 5
            }
        }
        # self.sprite_types = {
        #     'barrel': pg.image.load('sprites/barrel/0.png').convert_alpha(),
        #     'devil': [pg.image.load(f'sprites/Devil/{i}.png').convert_alpha() for i in range(8)]
        # }

        self.obj_list = \
            [
                SpriteObj(self.sprite_params['sprite_barrel'], (7.1, 2.1)),
                SpriteObj(self.sprite_params['sprite_barrel'], (5.9, 2.1)),
                SpriteObj(self.sprite_params['sprite_devil'], (7, 4)),
                SpriteObj(self.sprite_params['sprite_flame'], (7, 7))
            ]

class SpriteObj:
    def __init__(self, params, pos):
        self.obj = params['sprite']
        self.viewing_angles = params['viewing_angles']
        self.pos = self.x, self.y = pos[0] * TILE_WIDTH, pos[1] * TILE_WIDTH
        self.shift = params['shift']
        self.scale = params['scale']
        self.animation = params['animation']
        self.animation_dist = params['animation_dist']
        self.animation_speed = params['animation_speed']
        self.animation_counter = 0

        if self.viewing_angles:
            self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.obj)}


    def obj_detector(self, player):
        dx, dy = self.x - player.x, self.y - player.y
        dist_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        theta = math.atan2(dy, dx)
        gamma = theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += DOUBLE_PI

        dt_rays = int(gamma / dt_ANGLE)
        cur_ray = Center_RAY + dt_rays
        dist_to_sprite *= math.cos(HALF_FOV - cur_ray * dt_ANGLE)

        fake_ray = cur_ray + NONE_VISIABLE_RAYS

        if 0 <= fake_ray <= FAKE_RAYS_RANGE and dist_to_sprite > 30:
            proj_height = min(int(PROJECTION_C / dist_to_sprite * self.scale), DOUBLE_HEIGHT)
            half_projection_height = proj_height // 2
            shift = half_projection_height * self.shift

            if self.viewing_angles:
                if theta < 0:
                    theta += DOUBLE_PI
                theta = 360 - int(math.degrees(theta))

                for angles in self.sprite_angles:
                    if theta in angles:
                        self.obj = self.sprite_positions[angles]

            # Анимация спрайтов
            sprite_obj = self.obj
            if self.animation and dist_to_sprite < self.animation_dist:
                sprite_obj = self.animation[0]
                if self.animation_counter < self.animation_speed:
                    self.animation_counter += 1
                else:
                    self.animation.rotate()
                    self.animation_counter = 0

            # Проекция спрайта
            sprite_position = (cur_ray * SCALE - half_projection_height, HALF_HEIGHT - half_projection_height + shift)
            sprite = pg.transform.scale(sprite_obj, (proj_height, proj_height))

            return (dist_to_sprite, sprite, sprite_position)
        else:
            return (False,)