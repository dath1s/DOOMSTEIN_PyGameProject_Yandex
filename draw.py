import pygame as pg
from config import *
from ray_casting import ray_casting
from map import mini_map
from collections import deque
import sys
from random import randint


class Drawing:
    def __init__(self, sc, mini_map_surf, player, health_surf, clock):
        self.sc = sc
        self.player = player
        self.mini_map_surf = mini_map_surf
        self.health = health_surf
        self.clock = clock
        self.font = pg.font.SysFont('Arial', 48, bold=True)
        self.font_win = pg.font.Font('font/EternalLogo-51X9B.ttf', 100)
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
        self.shot_sound = pg.mixer.Sound('music/shotgun.wav')

        self.sfx = deque([pg.image.load(f'sprites/sfx/{i}.png').convert_alpha() for i in range(9)])
        self.sfx_length_count = 0
        self.sfx_length = len(self.sfx)

        self.menu_trigger = True
        self.menu_picture = pg.image.load('textures/bg.jpg').convert()

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

    # def fps_rate(self, clock):
    #     display_fps = str(int(clock.get_fps()))
    #     render = self.font.render(display_fps, False, colors["green"])
    #     self.sc.blit(render, (20, 20))

    # def pos(self, player):
    #     display_pos = f'x: {player.get_cur_pos()[0]}; y: {player.get_cur_pos()[1]}'
    #     render = self.font.render(display_pos, False, colors["green"])
    #     self.sc.blit(render, (20, 60))

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

    def draw_health(self, player):
        self.health.fill(colors["red"])
        pg.draw.line(self.health, colors["green"], (0, 22.5),
                     (player.health * 3, 22.5), 45)

        font = pg.font.SysFont(None, 72)
        hp = font.render('HP', True,
                  (255, 255, 255))

        self.sc.blit(self.health, (0, 0))
        self.sc.blit(hp, (0, 0))

    def player_weapon(self, shots):
        if self.player.shot:
            if not self.shot_length_count:
                self.shot_sound.play()
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

    def win(self):
        if self.player.health > 0:
            render = self.font_win.render('YOU WIN!!!', 1, (randint(40, 120), 0, 0))
            rect = pg.Rect(0, 0, 1000, 400)
            rect.center = HALF_WIDTH, HALF_HEIGHT
            pg.draw.rect(self.sc, colors['black'], rect, border_radius=50)
            self.sc.blit(render, (rect.centerx - 450, rect.centery - 100))
        else:
            render = self.font_win.render('YOU LOSE:(', 1, (randint(40, 120), 0, 0))
            rect = pg.Rect(0, 0, 1000, 400)
            rect.center = HALF_WIDTH, HALF_HEIGHT
            pg.draw.rect(self.sc, colors['black'], rect, border_radius=50)
            self.sc.blit(render, (rect.centerx - 450, rect.centery - 100))

        score = self.font_win.render('Score: ' + str(self.player.score), 1, (randint(40, 120), 0, 0))
        self.sc.blit(score, (rect.centerx - 450, rect.centery + 50))
        pg.display.flip()
        self.clock.tick(15)

    def menu(self):
        x = 0
        button_font = pg.font.Font('font/EternalLogo-51X9B.ttf', 72)
        label_font = pg.font.Font('font/EternalLogo-51X9B.ttf', 150)
        start = button_font.render('START', 1, pg.Color('lightgray'))
        button_start = pg.Rect(0, 0, 400, 150)
        button_start.center = HALF_WIDTH, HALF_HEIGHT
        exit = button_font.render('EXIT', 1, pg.Color('lightgray'))
        button_exit = pg.Rect(0, 0, 400, 150)
        button_exit.center = HALF_WIDTH, HALF_HEIGHT + 200

        while self.menu_trigger:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.sc.blit(self.menu_picture, (0, 0), (x % WIDTH, HALF_HEIGHT, WIDTH, HEIGHT))
            x += 1

            pg.draw.rect(self.sc, colors['black'], button_start, border_radius=25, width=10)
            self.sc.blit(start, (button_start.centerx - 160, button_start.centery - 50))

            pg.draw.rect(self.sc, colors['black'], button_exit, border_radius=25, width=10)
            self.sc.blit(exit, (button_exit.centerx - 105, button_exit.centery - 55))

            color = randint(0, 40)
            label = label_font.render('DOOMSTEIN', 1, (color, color, color))
            self.sc.blit(label, (15, -30))

            mouse_pos = pg.mouse.get_pos()
            mouse_click = pg.mouse.get_pressed()

            if button_start.collidepoint(mouse_pos):
                pg.draw.rect(self.sc, colors['black'], button_start, border_radius=25)
                self.sc.blit(start, (button_start.centerx - 130, button_start.centery - 70))

                if mouse_click[0]:
                    self.menu_trigger = False

            elif button_exit.collidepoint(mouse_pos):
                pg.draw.rect(self.sc, colors['black'], button_exit, border_radius=25)
                self.sc.blit(exit, (button_exit.centerx - 85, button_exit.centery - 70))

                if mouse_click[0]:
                    pg.quit()
                    sys.exit()

            pg.display.flip()
            self.clock.tick(20)