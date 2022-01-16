import pygame as pg
from config import *
from collections import deque
from ray_casting import select_cur_sector


class Sprites:
    def __init__(self):
        self.sprite_params = {
            'sprite_barrel': {
                'name': 'barrel',
                'sprite': pg.image.load('sprites/barrel/base/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 1.8,
                'scale': (0.4, 0.4),
                'animation': deque([
                    pg.image.load(f'sprites/barrel/anim/{i}.png').convert_alpha() for i in range(1)
                ]),
                'death_animation': deque([
                    pg.image.load(f'sprites/barrel/death/{i}.png').convert_alpha() for i in range(4)
                ]),
                'is_dead': None,
                'death_shift': 2.6,
                'animation_dist': 800,
                'animation_speed': 10,
                'blocked': True,
                'flag': 'decor',
                'obj_action': [],
                'side': 30
            },
            'sprite_devil': {
                'name': 'devil',
                'sprite': [pg.image.load(f'sprites/devil/base/{i}.png').convert_alpha() for i in range(8)],
                'viewing_angles': True,
                'shift': -0.2,
                'scale': (1.1, 1.1),
                'animation': [],
                'death_animation': deque([
                    pg.image.load(f'sprites/devil/death/{i}.png').convert_alpha() for i in range(6)
                ]),
                'is_dead': None,
                'death_shift': 0.6,
                'animation_dist': 150,
                'animation_speed': 10,
                'blocked': True,
                'flag': 'npc',
                'obj_action': deque([
                    pg.image.load(f'sprites/devil/anim/{i}.png').convert_alpha() for i in range(9)
                ]),
                'side': 50
            },
            'sprite_flame': {
                'name': 'flame',
                'sprite': pg.image.load('sprites/flame/base/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.7,
                'scale': (0.6, 0.6),
                'animation': deque(
                    [pg.image.load(f'sprites/flame/anim/{i}.png').convert_alpha() for i in range(16)]),
                'death_animation': [],
                'is_dead': 'immortal',
                'death_shift': 1.8,
                'animation_dist': 800,
                'animation_speed': 5,
                'blocked': False,
                'flag': 'decor',
                'obj_action': [],
                'side': 30
            },
            'sprite_door_h': {
                'name': 'door',
                'sprite': [pg.image.load(f'sprites/doors/door_h/{i}.png').convert_alpha() for i in range(16)],
                'viewing_angles': True,
                'shift': 0.1,
                'scale': (2.6, 1.2),
                'side': 100,
                'animation': [],
                'death_animation': [],
                'is_dead': 'immortal',
                'death_shift': 0,
                'animation_dist': 0,
                'animation_speed': 0,
                'blocked': True,
                'flag': 'door_v',
                'obj_action': []
            },
            'sprite_door_v': {
                'name': 'door',
                'sprite': [pg.image.load(f'sprites/doors/door_v/{i}.png').convert_alpha() for i in range(16)],
                'viewing_angles': True,
                'shift': 0.1,
                'scale': (2.6, 1.2),
                'side': 100,
                'animation': [],
                'death_animation': [],
                'is_dead': 'immortal',
                'death_shift': 0,
                'animation_dist': 0,
                'animation_speed': 0,
                'blocked': True,
                'flag': 'door_h',
                'obj_action': []
            },
            'npc_soldier0': {
                'name': 'soilder',
                'sprite': [pg.image.load(f'sprites/soilder/base/{i}.png').convert_alpha() for i in range(8)],
                'viewing_angles': True,
                'shift': 0.8,
                'scale': (0.4, 0.6),
                'side': 30,
                'animation': [],
                'death_animation': deque([pg.image.load(f'sprites/soilder/death/{i}.png')
                                         .convert_alpha() for i in range(11)]),
                'is_dead': None,
                'death_shift': 1.7,
                'animation_dist': None,
                'animation_speed': 6,
                'blocked': True,
                'flag': 'npc',
                'obj_action': deque([pg.image.load(f'sprites/soilder/action/{i}.png')
                                    .convert_alpha() for i in range(4)])
            },
            'npc_soldier1': {
                'name': 'soilder_c',
                'sprite': [pg.image.load(f'sprites/soilder/base/{i}.png').convert_alpha() for i in range(8)],
                'viewing_angles': True,
                'shift': 0.8,
                'scale': (0.4, 0.6),
                'side': 30,
                'animation': [],
                'death_animation': deque([pg.image.load(f'sprites/soilder/death/{i}.png')
                                         .convert_alpha() for i in range(11)]),
                'is_dead': None,
                'death_shift': 1.7,
                'animation_dist': None,
                'animation_speed': 6,
                'blocked': True,
                'flag': 'npc',
                'obj_action': deque([pg.image.load(f'sprites/soilder/action/{i}.png')
                                    .convert_alpha() for i in range(4)])
            },
        }
        # self.sprite_types = {
        #     'barrel': pg.image.load('sprites/barrel/0.png').convert_alpha(),
        #     'devil': [pg.image.load(f'sprites/Devil/{i}.png').convert_alpha() for i in range(8)]
        # }

        self.obj_list = \
            [
                SpriteObj(self.sprite_params['sprite_barrel'], (8.5, 5.5)),
                SpriteObj(self.sprite_params['sprite_barrel'], (8.5, 12.5)),
                SpriteObj(self.sprite_params['sprite_barrel'], (15.5, 5.5)),
                SpriteObj(self.sprite_params['sprite_barrel'], (15.5, 12.5)),
                SpriteObj(self.sprite_params['sprite_flame'], (12, 10.15)),
                SpriteObj(self.sprite_params['sprite_flame'], (12, 7.9)),
                SpriteObj(self.sprite_params['sprite_door_h'], (12.5, 5.5)),
                SpriteObj(self.sprite_params['sprite_door_h'], (11.5, 12.5)),
                SpriteObj(self.sprite_params['sprite_door_v'], (6.5, 15.5)),
                SpriteObj(self.sprite_params['sprite_door_v'], (5.5, 2.5)),
                SpriteObj(self.sprite_params['sprite_door_v'], (8.5, 8.5)),
                SpriteObj(self.sprite_params['sprite_door_v'], (15.5, 8.5)),
                SpriteObj(self.sprite_params['sprite_devil'], (20, 9.5)),
                SpriteObj(self.sprite_params['sprite_devil'], (22, 7.8)),
                SpriteObj(self.sprite_params['sprite_devil'], (23, 13)),
                SpriteObj(self.sprite_params['sprite_devil'], (22, 4)),
                SpriteObj(self.sprite_params['sprite_devil'], (14.5, 13.7)),
                SpriteObj(self.sprite_params['sprite_devil'], (11.5, 13.7)),
                SpriteObj(self.sprite_params['sprite_devil'], (12, 3)),
                SpriteObj(self.sprite_params['sprite_devil'], (5, 11)),
                SpriteObj(self.sprite_params['npc_soldier1'], (14, 9)),
                SpriteObj(self.sprite_params['npc_soldier1'], (14, 7.5)),
                SpriteObj(self.sprite_params['npc_soldier1'], (14, 10)),
                SpriteObj(self.sprite_params['npc_soldier0'], (17, 15)),
                SpriteObj(self.sprite_params['npc_soldier0'], (7, 7)),
                SpriteObj(self.sprite_params['npc_soldier0'], (12, 14)),
                SpriteObj(self.sprite_params['npc_soldier0'], (9, 14.5)),
                SpriteObj(self.sprite_params['npc_soldier1'], (15, 14.5)),
                SpriteObj(self.sprite_params['npc_soldier1'], (8, 3)),
                SpriteObj(self.sprite_params['npc_soldier0'], (5.5, 14.5))
            ]

    @property
    def sprite_shot(self):
        return min([obj.is_on_fireway for obj in self.obj_list], default=(float('inf'), 0))

    @property
    def blocked_doors(self):
        blocked_doors = {}
        for obj in self.obj_list:
            if obj.flag in {'door_h', 'door_v'} and obj.blocked:
                i, j = select_cur_sector(obj.x, obj.y)
                blocked_doors[(i, j)] = 0
        return blocked_doors


class SpriteObj:
    def __init__(self, params, pos):
        self.obj = params['sprite'].copy()
        self.viewing_angles = params['viewing_angles']
        self.shift = params['shift']
        self.scale = params['scale']
        self.animation = params['animation'].copy()

        self.death_animation = params['death_animation'].copy()
        self.is_dead = params['is_dead']
        self.dead_shift = params['death_shift']

        self.animation_dist = params['animation_dist']
        self.animation_speed = params['animation_speed']

        self.blocked = params['blocked']
        self.flag = params['flag']
        self.obj_action = params['obj_action'].copy()
        self.x, self.y = pos[0] * TILE_WIDTH, pos[1] * TILE_WIDTH
        self.side = params['side']

        self.dead_animation_count = 0
        self.animation_counter = 0

        self.npc_action_trigger = False
        self.door_open_trigger = False

        self.door_prev_pos = self.y if self.flag == 'door_h' else self.x

        self.delete = False

        self.name = params['name']

        if self.viewing_angles:
            if len(self.obj) == 8:
                self.sprite_angles = [frozenset(range(338, 361)) | frozenset(range(0, 23))] + \
                                     [frozenset(range(i, i + 45)) for i in range(23, 338, 45)]
            else:
                self.sprite_angles = [frozenset(range(348, 361)) | frozenset(range(0, 11))] + \
                                     [frozenset(range(i, i + 23)) for i in range(11, 348, 23)]
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
        self.theta -= 1.4 * gamma

        dt_rays = int(gamma / dt_ANGLE)
        self.cur_ray = Center_RAY + dt_rays
        if self.flag not in {'door_h', 'door_v'}:
            self.dist_to_sprite *= math.cos(HALF_FOV - self.cur_ray * dt_ANGLE)

        fake_ray = self.cur_ray + NONE_VISIABLE_RAYS

        if 0 <= fake_ray <= FAKE_RAYS_RANGE and self.dist_to_sprite > 30:
            self.proj_height = min(int(PROJECTION_C / self.dist_to_sprite),
                                   DOUBLE_HEIGHT if self.flag not in {'door_h', 'door_v'} else HEIGHT)
            sprite_width = int(self.proj_height * self.scale[0])
            sprite_height = int(self.proj_height * self.scale[1])
            half_sprite_width = sprite_width // 2
            half_sprite_height = sprite_height // 2
            shift = half_sprite_height * self.shift

            if self.flag in {'door_h', 'door_v'}:
                if self.door_open_trigger:
                    self.open_door()
                self.obj = self.visible_sprite()
                sprite_object = self.sprite_animation()
            else:
                if self.is_dead and self.is_dead != 'immortal':
                    sprite_object = self.death_animation_player()
                    shift = half_sprite_height * self.dead_shift
                    sprite_height = int(sprite_height / 1.3)
                elif self.npc_action_trigger:
                    sprite_object = self.npc_action()
                else:
                    self.obj = self.visible_sprite()
                    sprite_object = self.sprite_animation()

            # Проекция спрайта
            sprite_position = (
            self.cur_ray * SCALE - half_sprite_width, HALF_HEIGHT - half_sprite_height + shift)
            sprite = pg.transform.scale(sprite_object, (sprite_width, sprite_height))

            return (self.dist_to_sprite, sprite, sprite_position, None)
        else:
            return (False,)

    def sprite_animation(self):
        if self.animation and self.dist_to_sprite < self.animation_dist:
            sprite_obj = self.animation[0]
            if self.animation_counter < self.animation_speed:
                self.animation_counter += 1
            else:
                self.animation.rotate()
                self.animation_counter = 0
            return sprite_obj
        return self.obj

    def visible_sprite(self):
        if self.viewing_angles:
            if self.theta < 0:
                self.theta += DOUBLE_PI
            self.theta = 360 - int(math.degrees(self.theta))

            for angles in self.sprite_angles:
                if self.theta in angles:
                    return self.sprite_positions[angles]
        return self.obj

    def death_animation_player(self):
        if len(self.death_animation):
            if self.dead_animation_count < self.animation_speed:
                self.dead_sprite = self.death_animation[0]
                self.dead_animation_count += 1
            else:
                self.dead_sprite = self.death_animation.popleft()
                self.dead_animation_count = 0
        return self.dead_sprite

    def npc_action(self):
        sprite_object = self.obj_action[0]
        if self.animation_counter < self.animation_speed:
            self.animation_counter += 1
        else:
            self.obj_action.rotate()
            self.animation_counter = 0
        return sprite_object

    def open_door(self):
        if self.flag == 'door_h':
            self.y -= 3
            if abs(self.y - self.door_prev_pos) > TILE_WIDTH:
                self.delete = True
        elif self.flag == 'door_v':
            self.x -= 3
            if abs(self.x - self.door_prev_pos) > TILE_WIDTH:
                self.delete = True
