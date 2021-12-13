import pygame as pg
from config import *


class Sprites:
    def __init__(self):
        self.sprite_types = {
            'barrel': pg.image.load('sprites/barrel/0.png').convert_alpha()
        }
        self.obj_list = \
            [
                SpriteObj(self.sprite_types['barrel'], True, (7.1, 2.1), 1.8, 0.4),
                SpriteObj(self.sprite_types['barrel'], True, (5.9, 2.1), 1.8, 0.4)
            ]

class SpriteObj:
    def __init__(self, obj, is_static, pos, shift, scale):
        self.obj = obj
        self.is_static = is_static
        self.pos = self.x, self.y = pos[0] * TILE_WIDTH, pos[1] * TILE_WIDTH
        self.shift = shift
        self.scale = scale

    def obj_detector(self, player, walls):
        dx, dy = self.x - player.x, self.y - player.y
        dist_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        theta = math.atan2(dy, dx)
        gamma = theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += DOUBLE_PI

        dt_rays = int(gamma / dt_ANGLE)
        cur_ray = Center_RAY + dt_rays
        dist_to_sprite *= math.cos(HALF_FOV - cur_ray * dt_ANGLE)

        if 0 <= cur_ray <= NUM_OF_RAYS - 1 and dist_to_sprite < walls[cur_ray][0]:
            proj_height = int(PROJECTION_C / dist_to_sprite * self.scale)
            half_projection_height = proj_height // 2
            shift = half_projection_height * self.shift

            sprite_position = (cur_ray * SCALE - half_projection_height, HALF_HEIGHT - half_projection_height + shift)
            sprite = pg.transform.scale(self.obj, (proj_height, proj_height))

            return (dist_to_sprite, sprite, sprite_position)

        else:
            return (False,)