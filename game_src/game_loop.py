from random import randint

import pygame

from game_src.level_handler import create_level
from game_src.pause_screen import pause_screen
from sprites_classes.dead_frog import Dead_Frog
from image.image_handler import get_player_sprite, get_get_sprite, get_mob_sprite, \
    get_life_sprite, get_dead_sprite, get_beer_sprite, get_floating_mob_sprite

from sprites_classes.npc import Mob, Goat, Floating_mob
from sprites_classes.player import Player
from quiz_ui.quiz_handler import quiz_window, quiz
from music_and_sound.sound_handler import get_level_music, get_goat_music, get_drunk_music
from game_src.window_handler import screen, lose_window, win_window


# This function updates the window with sprites_classes each loop
def redraw_window(animals, wise_goat, dead_frog, background_image, lanes, floating_lanes):
    screen.blit(background_image, (0, 0))
    screen.blit(get_life_sprite(), (10, 315))
    screen.blit(pygame.transform.flip(get_life_sprite(), True, True), (10, 205))
    life_x = 10
    beer_y = 285
    for i in range(animals.drunk_meter):
        screen.blit(get_beer_sprite(), (10, beer_y))
        beer_y -= 25
    for i in range(animals.lives):
        screen.blit(get_life_sprite(), (life_x, 10))
        life_x += 25
    for lane in floating_lanes:
        for mob in lane.floating_mobs:
            screen.blit(mob.image, mob.mob_rect)

    if dead_frog.is_dead:
        screen.blit(dead_frog.img, (dead_frog.dead_x, dead_frog.dead_y))
        screen.blit(animals.update_img()[0], (1000, 1000))

    else:
        screen.blit(animals.update_img()[0], animals.update_img()[1])
    for lane in lanes:
        for car in lane.mobs:
            screen.blit(car.image, car.mob_rect)
    # screen.blit(get_get_sprite(), (animals.player_x - 20, wise_goat.get_y))
    pygame.display.update()


# This function runs the main game
def game_loop(sound_fx, volume):
    clock = pygame.time.Clock()
    get_level_music()
    animals = Player(400, 570, 40, 30, 0, get_player_sprite(0))
    dead_frog = Dead_Frog()
    wise_goat = Goat(animals.player_x, 200, 40, 30)
    pygame.display.set_caption("Drunk Frogger")

    q = True

    level_number = 1
    while True:
        level = create_level(level_number)
        running = True
        while running:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            level.update_lanes()
            level.spawn_mobs()

            keys = pygame.key.get_pressed()
            if dead_frog.is_dead:
                dead_frog.check_time_of_death()
            else:
                animals.move(keys)
            if keys[pygame.K_p]:
                level.spawn_paused()
                volume = pause_screen(volume)
                level.spawn_resumed()
                # volume = Sound_settings(volume)
                if not volume:
                    return
            for lane in level.lanes:
                for car in lane.mobs:
                    if animals.check_collide(car):
                        if animals.lives != 1:
                            animals.lives -= 1
                            dead_frog.player_died(animals.player_x, animals.player_y)
                            sound_fx.play_splat()
                            animals.reset()
                        else:
                            lose_window()
                            return
            animals.floating = False
            for lane in reversed(level.floating_lanes):
                if animals.floating == False:
                    for floating_mob in lane.floating_mobs:
                        if animals.check_collide(floating_mob):
                            animals.floating = True
                            if lane.is_left:
                                animals.player_x -= lane.velocity
                            else:
                                animals.player_x += lane.velocity
                            break
                        else:
                            animals.floating = False

            if animals.player_y < 225 and not animals.floating:
                if animals.lives != 1:
                    animals.lives -= 1
                    dead_frog.player_died(animals.player_x, animals.player_y)
                    sound_fx.play_splat()
                    animals.reset()
                else:
                    lose_window()
                    return

            # This if statement checks if the player has reached the safe zone and triggers the quiz function
            if animals.player_y <= 300 and q is False:
                get_goat_music()
                level.spawn_paused()

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
                    animals.reset()
                    running = False
                level.spawn_resumed()

            redraw_window(animals, wise_goat, dead_frog, level.background_image, level.lanes, level.floating_lanes)
        if level_number == 3:
            level_number = 1
