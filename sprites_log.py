import pygame as pg
from config import *


class Sprites:
    def __init__(self):
        self.sprite_types = {
            'barrel': pg.image.load('sprites/barrel/0.png').convert_alpha(),
            'devil': [pg.image.load(f'sprites/Devil/{i}.png').convert_alpha() for i in range(8)]
        }
        self.obj_list = \
            [
                SpriteObj(self.sprite_types['barrel'], True, (7.1, 2.1), 1.8, 0.4),
                SpriteObj(self.sprite_types['barrel'], True, (5.9, 2.1), 1.8, 0.4),
                SpriteObj(self.sprite_types['devil'], False, (7, 4), -0.2, 0.7)
            ]

class SpriteObj:
    def __init__(self, obj, is_static, pos, shift, scale):
        self.obj = obj
        self.is_static = is_static
        self.pos = self.x, self.y = pos[0] * TILE_WIDTH, pos[1] * TILE_WIDTH
        self.shift = shift
        self.scale = scale

        if not is_static:
            self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.obj)}


    def obj_detector(self, player, walls):
        none_render_walls_FST = [walls[0] for _ in range(NONE_VISIABLE_RAYS)]
        none_render_walls_SCND = [walls[-1] for _ in range(NONE_VISIABLE_RAYS)]
        none_render_walls = none_render_walls_FST + walls + none_render_walls_SCND

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

        if 0 <= fake_ray <= NUM_OF_RAYS - 1 + 2 * NONE_VISIABLE_RAYS and dist_to_sprite < none_render_walls[fake_ray][0]:
            proj_height = int(PROJECTION_C / dist_to_sprite * self.scale)
            half_projection_height = proj_height // 2
            shift = half_projection_height * self.shift

            if not self.is_static:
                if theta < 0:
                    theta += DOUBLE_PI
                theta = 360 - int(math.degrees(theta))

                for angles in self.sprite_angles:
                    if theta in angles:
                        self.obj = self.sprite_positions[angles]

            sprite_position = (cur_ray * SCALE - half_projection_height, HALF_HEIGHT - half_projection_height + shift)
            sprite = pg.transform.scale(self.obj, (proj_height, proj_height))

            return (dist_to_sprite, sprite, sprite_position)

        else:
            return (False,)