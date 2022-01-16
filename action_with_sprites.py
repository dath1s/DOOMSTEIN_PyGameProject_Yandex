from config import *
from player_settings import *
from map import world_map
from ray_casting import select_cur_sector
import math
import pygame as pg
from map import walls_collision


def ray_casting_npc_player(npc_x, npc_y, blocked_doors, world_map, player_pos):
    ox, oy = player_pos
    xm, ym = select_cur_sector(ox, oy)
    delta_x, delta_y = ox - npc_x, oy - npc_y
    cur_angle = math.atan2(delta_y, delta_x)
    cur_angle += math.pi

    sin_a = math.sin(cur_angle)
    sin_a = sin_a if sin_a else 0.000001
    cos_a = math.cos(cur_angle)
    cos_a = cos_a if cos_a else 0.000001

    # verticals
    x, dx = (xm + TILE_WIDTH, 1) if cos_a >= 0 else (xm, -1)
    for i in range(0, int(abs(delta_x)) // TILE_WIDTH):
        depth_v = (x - ox) / cos_a
        yv = oy + depth_v * sin_a
        tile_v = select_cur_sector(x + dx, yv)
        if tile_v in world_map or tile_v in blocked_doors:
            return False
        x += dx * TILE_WIDTH

    # horizontals
    y, dy = (ym + TILE_WIDTH, 1) if sin_a >= 0 else (ym, -1)
    for i in range(0, int(abs(delta_y)) // TILE_WIDTH):
        depth_h = (y - oy) / sin_a
        xh = ox + depth_h * cos_a
        tile_h = select_cur_sector(xh, y + dy)
        if tile_h in world_map or tile_h in blocked_doors:
            return False
        y += dy * TILE_WIDTH
    return True


class Interaction:
    def __init__(self, player, sprites, drawing):
        self.player = player
        self.sprites = sprites
        self.drawing = drawing

        self.attack_time = 15
        self.dt_attack = 0
        self.pain_sound = pg.mixer.Sound('music/pain.wav')

    def interaction_objects(self):
        if self.player.shot and self.drawing.shot_animation_trigger:
            for obj in sorted(self.sprites.obj_list, key=lambda obj: obj.dist_to_sprite):
                if obj.is_on_fireway[1]:
                    if obj.is_dead != 'immortal' and not obj.is_dead:
                        self.player.score += 10
                        if ray_casting_npc_player(obj.x, obj.y,
                                                  self.sprites.blocked_doors,
                                                  world_map, (self.player.x, self.player.y)):
                            if obj.flag == 'npc':
                                self.pain_sound.play()
                            obj.is_dead = True
                            obj.blocked = None
                            self.drawing.shot_animation_trigger = False
                    if obj.flag in {'door_h', 'door_v'} and obj.dist_to_sprite < TILE_WIDTH:
                        obj.door_open_trigger = True
                        obj.blocked = None
                    break

    def npc_action(self):
        for obj in self.sprites.obj_list:
            if obj.flag == 'npc' and not obj.is_dead:
                if ray_casting_npc_player(obj.x, obj.y,
                                          self.sprites.blocked_doors,
                                          world_map, (self.player.x, self.player.y)):
                    obj.npc_action_trigger = True
                    self.npc_move(obj)
                else:
                    obj.npc_action_trigger = False

    def npc_move(self, obj):
        if obj.name == 'devil':
            if abs(obj.dist_to_sprite) > TILE_WIDTH:
                dx = obj.x - self.player.x
                dy = obj.y - self.player.y
                obj.x = obj.x + 1 if dx < 0 else obj.x - 1
                obj.y = obj.y + 1 if dy < 0 else obj.y - 1
            else:
                if self.dt_attack < self.attack_time:
                    self.dt_attack += 1
                else:
                    self.player.health -= 10
                    self.dt_attack = 0

    def clear_world(self):
        deleted_objects = self.sprites.obj_list[:]
        [self.sprites.obj_list.remove(obj) for obj in deleted_objects if obj.delete]

    def play_music(self):
        pg.mixer.pre_init(44100, -16, 2, 2048)
        pg.mixer.init()
        pg.mixer.music.load('music/theme.mp3')
        pg.mixer.music.play(10)

    def check_win(self):
        if not len([obj for obj in self.sprites.obj_list if obj.flag == 'npc' and not obj.is_dead]):
            pg.mixer.music.stop()
            pg.mixer.music.load('music/win.mp3')
            pg.mixer.music.play()
            while True:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        exit()
                self.drawing.win()

        elif self.player.health <= 0:
            pg.mixer.music.stop()
            pg.mixer.music.load('music/win.mp3')
            pg.mixer.music.play()
            while True:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        exit()
                self.drawing.win()