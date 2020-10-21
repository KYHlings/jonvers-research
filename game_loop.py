import sys
from random import randint

import pygame

from dead_frog import Dead_Frog
from image_handler import get_player_sprite, get_get_sprite, get_mob_sprite, get_background_image, get_life_sprite, \
    get_dead_sprite, get_log_sprite

from npc import Mob, Get, FloatingMob
from player import Player
from quiz_handler import quiz_window, quiz
from settings import Sound_settings
from sound_handler import get_level_music, get_goat_music, get_drunk_music
from window_handler import screen, lose_window, win_window


# This function updates the window with sprites each loop
def redraw_window(cars, animals, wise_goat, dead_frog, logs):
    life_x = 10
    for log in logs:
        screen.blit(log.image, (log.mob_rect))
        log.hitbox = (log.x + 6, log.y + 7, 69, 30)
        # pygame.draw.rect(screen, (255, 0, 0), log.hitbox, 3)
    for i in range(animals.lives):
        screen.blit(get_life_sprite(), (life_x, 10))
        life_x += 25
    if dead_frog.is_dead:
        screen.blit(dead_frog.img, (dead_frog.dead_x, dead_frog.dead_y))
        screen.blit(animals.update_img()[0], (1000, 1000))

    else:
        screen.blit(animals.update_img()[0], animals.update_img()[1])
    for car in cars:
        screen.blit(car.image, (car.mob_rect))
        car.hitbox = (car.x + 6, car.y + 7, 69, 30)
        # pygame.draw.rect(screen, (255, 0, 0), car.hitbox, 3)

    screen.blit(get_get_sprite(), (animals.player_x - 20, wise_goat.get_y))
    pygame.display.update()


# This function runs the main game
def game_loop(sound_fx, volume):
    clock = pygame.time.Clock()
    get_level_music()
    animals = Player(400, 570, 40, 30, 0, get_player_sprite(0))
    cars = [Mob(0, 350, 80, 40, get_mob_sprite(False)), Mob(0, 400, 80, 40, get_mob_sprite(True)),
            Mob(0, 450, 80, 40, get_mob_sprite(False))]
    logs = [FloatingMob(0, 700, get_log_sprite(False))]

    dead_frog = Dead_Frog()
    wise_goat = Get(animals.player_x, 200, 40, 30)
    pygame.display.set_caption("Drunk Frogger")
    running = True

    now_cars = [pygame.time.get_ticks(), pygame.time.get_ticks(), pygame.time.get_ticks()]
    now_logs = [pygame.time.get_ticks()]
    mob_spawn_timer = [1000, 2000, 1000]
    log_spawn_timer = [1000]
    lanes = [350, 400, 450]
    water_lane = [130]
    q = True
    while running:
        clock.tick(30)
        screen.blit(get_background_image(), (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for log in logs[:]:
            if log.y != 400:
                log.update_rect(1)
                if log.x >= 800:
                    logs.remove(log)
            else:
                log.update_rect(-1)
                if log.x <= -50:
                    logs.remove(log)
        for i in range(len(water_lane)):
            if pygame.time.get_ticks() - now_logs[i] >= log_spawn_timer[i]:
                logs.append(FloatingMob(0, water_lane[i], get_log_sprite(False)))
                now_logs[i] = pygame.time.get_ticks()
                log_spawn_timer[i] = randint(1000, 2000)

        for car in cars[:]:
            if car.y != 400:
                car.update_rect(1)
                if car.x >= 800:
                    cars.remove(car)
            else:
                car.update_rect(-1)
                if car.x <= -50:
                    cars.remove(car)
        for i in range(3):
            if pygame.time.get_ticks() - now_cars[i] >= mob_spawn_timer[i]:
                if lanes[i] != 400:
                    cars.append(Mob(0, lanes[i], 80, 40, get_mob_sprite(False)))
                else:
                    cars.append(Mob(800, lanes[i], 80, 40, get_mob_sprite(True)))
                now_cars[i] = pygame.time.get_ticks()
                mob_spawn_timer[i] = randint(1000, 2000)
        keys = pygame.key.get_pressed()
        if dead_frog.is_dead:
            dead_frog.check_time_of_death()
        else:
            animals.move(keys)
        if keys[pygame.K_p]:
            volume = Sound_settings(volume)
            if not volume:
                return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        for car in cars:
            if animals.check_collide(car):
                if animals.lives == 0:
                    lose_window()
                    return
                else:
                    dead_frog.player_died(animals.player_x, animals.player_y)
                    sound_fx.play_splat()
                    animals.reset()
        for log in logs:
            if animals.check_float_collide(log):
                animals.floating = True
                animals.player_x += log.velocity
                break
            else:
                animals.floating = False
        print(animals.floating)
        if animals.player_y < 180 and not animals.floating:
            if animals.lives == 0:
                lose_window()
                return
            else:
                dead_frog.player_died(animals.player_x, animals.player_y)
                sound_fx.play_splat()
                animals.reset()

            # This if statement checks if the player has reached the safe zone and triggers the quiz function
        if animals.player_y <= 300 and q == False:
            get_goat_music()

            # This if statement checks if the player answers correctly. If the player answers correctly they trigger the win function
            # if they do not answer correctly they get moved to the start position and adds one to the drunk_meter integer
            if not quiz_window(quiz()):
                if animals.drunk_meter == 3:
                    lose_window()
                    return
                animals.drunk_meter += 1
                dead_frog.img = get_dead_sprite(animals.drunk_meter)
                sound_fx.play_burp()
                animals.drunken_consequence()
                get_drunk_music(animals.drunk_meter)
                animals.reset()
                q = False
            else:
                win_window()
                return

        redraw_window(cars, animals, wise_goat, dead_frog, logs)
