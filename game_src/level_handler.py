from random import randint

import pygame

from image.image_handler import get_background_image, get_mob_sprite, get_floating_mob_sprite
from sprites_classes.npc import Mob, Goat, Floating_mob


class Level:
    def __init__(self, lanes, floating_lanes, background_image, goat, music, spawn_timer, time_spawned,
                 fl_spawn_timer, fl_time_spawned, drown_cord, paused_time):
        self.lanes = lanes
        self.floating_lanes = floating_lanes
        self.background_image = background_image
        self.goat = goat
        self.music = music
        self.spawn_timer = spawn_timer
        self.time_spawned = time_spawned
        self.fl_spawn_timer = fl_spawn_timer
        self.fl_time_spawned = fl_time_spawned
        self.drown_cord = drown_cord
        self.paused_time = paused_time

    def spawn_paused(self):
        self.paused_time = pygame.time.get_ticks()

    def spawn_resumed(self):
        print(self.time_spawned)
        extra_time = pygame.time.get_ticks() - self.paused_time
        for i in range(len(self.time_spawned)):
            self.time_spawned[i] += extra_time
        for i in range(len(self.fl_time_spawned)):
            self.fl_time_spawned[i] += extra_time
        print(self.time_spawned)

    def update_lanes(self):
        for lane in self.lanes + self.floating_lanes:
            for mob in lane.mobs[:]:
                if not mob.is_left:
                    mob.update_rect(1, lane.velocity)
                    if mob.mob_x >= 800:
                        lane.mobs.remove(mob)
                else:
                    mob.update_rect(-1, lane.velocity)
                    if mob.mob_x <= -50:
                        lane.mobs.remove(mob)

    def spawn_mobs(self):
        for i in range(len(self.lanes)):
            if pygame.time.get_ticks() - self.time_spawned[i] >= self.spawn_timer[i]:
                if not self.lanes[i].is_left:
                    self.lanes[i].mobs.append(
                        Mob(-40, self.lanes[i].y, get_mob_sprite(False), self.lanes[i].is_left))
                else:
                    self.lanes[i].mobs.append(
                        Mob(800, self.lanes[i].y, get_mob_sprite(True), self.lanes[i].is_left))
                self.time_spawned[i] = pygame.time.get_ticks()
                self.spawn_timer[i] = randint(3000, 3001)

        for i in range(len(self.floating_lanes)):
            if pygame.time.get_ticks() - self.fl_time_spawned[i] >= self.fl_spawn_timer[i]:
                if not self.floating_lanes[i].is_left:
                    self.floating_lanes[i].floating_mobs.append(
                        Floating_mob(-40, self.floating_lanes[i].y, get_floating_mob_sprite(False),
                                     self.floating_lanes[i].is_left))
                else:
                    self.floating_lanes[i].floating_mobs.append(
                        Floating_mob(800, self.floating_lanes[i].y, get_floating_mob_sprite(True),
                                     self.floating_lanes[i].is_left))
                self.fl_time_spawned[i] = pygame.time.get_ticks()
                self.fl_spawn_timer[i] = randint(1000, 2000)


class Lane:
    def __init__(self, mobs, y, velocity, is_left):
        self.mobs = mobs
        self.y = y
        self.velocity = velocity
        self.is_left = is_left
        self.floating_mobs = mobs


def create_level(level_number):
    if level_number == 1:
        level = Level(lanes=[Lane([Mob(0, 345, get_mob_sprite(False), False)], 345, 6, False),
                             Lane([Mob(500, 390, get_mob_sprite(True), True)], 390, 5, True),
                             Lane([Mob(0, 435, get_mob_sprite(False), False)], 435, 3, False),
                             Lane([Mob(600, 485, get_mob_sprite(True), True)], 485, 5, True)],
                      floating_lanes=[Lane([], 55, 5, True), Lane([], 85, 5, False), Lane([], 115, 5, True),
                                      Lane([], 145, 5, False), Lane([], 175, 3, True), Lane([], 200, 2, False)],
                      background_image=get_background_image(0),
                      goat=Goat(400, 200, 40, 30),
                      music=0,
                      spawn_timer=[1000, 2000, 1000, 2000],
                      time_spawned=[pygame.time.get_ticks(), pygame.time.get_ticks(), pygame.time.get_ticks(),
                                    pygame.time.get_ticks()],
                      fl_spawn_timer=[1000, 2000, 1000, 2000, 1000, 2000],
                      fl_time_spawned=[pygame.time.get_ticks(), pygame.time.get_ticks(), pygame.time.get_ticks(),
                                       pygame.time.get_ticks(), pygame.time.get_ticks(), pygame.time.get_ticks()],
                      drown_cord=225,
                      paused_time=0
                      )

    if level_number == 2:
        level = Level(lanes=[Lane([Mob(0, 350, get_mob_sprite(False), False)], 350, 5, False),
                             Lane([Mob(0, 400, get_mob_sprite(True), True)], 400, 5, True),
                             Lane([Mob(0, 450, get_mob_sprite(False), False)], 450, 5, False)],
                      background_image=get_background_image(1),
                      goat=Goat(400, 200, 40, 30),
                      music=0,
                      spawn_timer=[1000, 2000, 1000],
                      time_spawned=[pygame.time.get_ticks(), pygame.time.get_ticks(), pygame.time.get_ticks()],
                      drown_cord=0,
                      fl_spawn_timer=[],
                      fl_time_spawned=[],
                      floating_lanes=[],
                      paused_time=0
                      )

    if level_number == 3:
        pass
        # To be continued
    return level
