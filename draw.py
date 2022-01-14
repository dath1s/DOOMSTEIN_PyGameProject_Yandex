import pygame as pg
from config import *
from ray_casting import ray_casting
from map import mini_map
from collections import deque


class Drawing:
    def __init__(self, sc, mini_map_surf, player):
        self.sc = sc
        self.player = player
        self.mini_map_surf = mini_map_surf
        self.font = pg.font.SysFont('Arial', 48, bold=True)
        self.textures = {
            1: pg.image.load('textures/wall1.png').convert(),
            2: pg.image.load('textures/wall2.png').convert(),
            "sky": pg.image.load('textures/sky.png').convert()
        }

        self.weapon_base_sprite = pg.image.load('sprites/shotgun/base/0.png').convert_alpha()
        self.weapon_shot_animation = deque(
            [pg.image.load(f'sprites/shotgun/shot/{i}.png').convert_alpha() for i in range(20)])
        self.weapon_rect = self.weapon_base_sprite.get_rect()
        self.weapon_pos = (HALF_WIDTH - self.weapon_rect.width // 2,
                           HEIGHT - self.weapon_rect.height)
        self.shot_length = len(self.weapon_shot_animation)
        self.shot_length_count = 0
        self.shot_animation_speed = 3
        self.shot_animation_count = 0
        self.shot_animation_trigger = True

        self.sfx = deque([pg.image.load(f'sprites/sfx/{i}.png').convert_alpha() for i in range(9)])
        self.sfx_length_count = 0
        self.sfx_length = len(self.sfx)

    def draw_background(self, angle):
        # Отрисовка неба и пола
        sky_offset = -10 * math.degrees(angle) % WIDTH
        self.sc.blit(self.textures['sky'], (sky_offset, 0))
        self.sc.blit(self.textures['sky'], (sky_offset - WIDTH, 0))
        self.sc.blit(self.textures['sky'], (sky_offset + WIDTH, 0))

        pg.draw.rect(self.sc, (40, 40, 40), (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def draw_map(self, world_obj):
        for obj in sorted(world_obj, key=lambda x: x[0], reverse=True):
            if obj[0]:
                _, cur_obj, cur_obj_pos, p_height = obj
                self.sc.blit(cur_obj, cur_obj_pos)

    def fps_rate(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, False, colors["green"])
        self.sc.blit(render, (20, 20))

    def pos(self, player):
        display_pos = f'x: {player.get_cur_pos()[0]}; y: {player.get_cur_pos()[1]}'
        render = self.font.render(display_pos, False, colors["green"])
        self.sc.blit(render, (20, 60))

    def draw_mini_map(self, player):
        self.mini_map_surf.fill(colors["black"])
        player_x, player_y = player.x // MAP_SCALE, player.y // MAP_SCALE
        pg.draw.line(self.mini_map_surf, colors["green"], (player_x, player_y),
                     (player_x + 20 * math.cos(player.angle),
                      player_y + 20 * math.sin(player.angle)), 5)
        for x, y in mini_map:
            pg.draw.rect(self.mini_map_surf, (1, 50, 32), (x, y, TILE_WIDTH // MAP_SCALE, TILE_WIDTH // MAP_SCALE))
        pg.draw.circle(self.mini_map_surf, colors["yellow"], (int(player_x), player_y), 5)
        self.sc.blit(self.mini_map_surf, MAP_POS)

    def player_weapon(self, shots):
        if self.player.shot:
            self.shot_projection = min(shots)[1] // 2
            self.bullet_sfx()
            shot_sprite = self.weapon_shot_animation[0]
            self.sc.blit(shot_sprite, self.weapon_pos)
            self.shot_animation_count += 1
            if self.shot_animation_count == self.shot_animation_speed:
                self.weapon_shot_animation.rotate(-1)
                self.shot_animation_count = 0
                self.shot_length_count += 1
                self.shot_animation_trigger = False
            if self.shot_length_count == self.shot_length:
                self.player.shot = False
                self.shot_length_count = 0
                self.sfx_length_count = 0
                self.shot_animation_trigger = True
        else:
            self.sc.blit(self.weapon_base_sprite, self.weapon_pos)

    def bullet_sfx(self):
        if self.sfx_length_count < self.sfx_length:
            sfx = pg.transform.scale(self.sfx[0], (self.shot_projection, self.shot_projection))
            sfx_rect = sfx.get_rect()
            self.sc.blit(sfx, (HALF_WIDTH - sfx_rect.w // 2, HALF_HEIGHT - sfx_rect.h // 2))
            self.sfx_length_count += 1
            self.sfx.rotate(-1)
