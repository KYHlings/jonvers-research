import pygame


def get_player_sprite(degree):


    player_sprite = pygame.image.load("images_src/frog.png")
    player_sprite = pygame.transform.scale(player_sprite, (40, 30))
    #player_sprite = pygame.transform.flip(player_sprite, False, False)
    player_sprite = pygame.transform.rotate(player_sprite, degree)
    return player_sprite


def get_background_image():
    background_image = pygame.image.load("images_src/back_placehold2.png")
    background_image = pygame.transform.scale(background_image, (800, 600))
    return background_image

def get_mob_sprite():
    mob_sprite = pygame.image.load("images_src/lorry.png")
    mob_sprite = pygame.transform.scale(mob_sprite,(80,40))
    return mob_sprite