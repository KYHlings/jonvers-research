import pygame


class Mob:
    def __init__(self, mob_x, mob_y, width, height, image):
        self.x = mob_x
        self.y = mob_y
        self.image = image
        self.width = width
        self.height = height
        self.velocity = 5
        self.hitbox = (self.x + 6, self.y + 7, 69, 30)
        self.mob_mask = pygame.mask.from_surface(self.image)
        self.mob_rect = self.image.get_rect(topleft=(self.x, self.y))

    def update_rect(self, direction):
        self.x += self.velocity * direction
        self.mob_rect = self.image.get_rect(topleft=(self.x, self.y))


class FloatingMob():
    def __init__(self, mob_x, mob_y, image):
        self.x = mob_x
        self.y = mob_y
        self.image = image[0]
        self.width, self.height = image[1]
        self.velocity = 5
        self.hitbox = (self.x + 6, self.y + 7, 69, 30)
        self.mob_mask = pygame.mask.from_surface(self.image)
        self.mob_rect = self.image.get_rect(topleft=(self.x, self.y))

    def update_rect(self, direction):
        self.x += self.velocity * direction
        self.mob_rect = self.image.get_rect(topleft=(self.x, self.y))


class Get:
    def __init__(self, get_x, get_y, width, height):
        self.get_x = get_x
        self.get_y = get_y
        self.width = width
        self.height = height
        self.velocity = 4
        self.hitbox = (self.get_x + 6, self.get_y + 7, 69, 30)
