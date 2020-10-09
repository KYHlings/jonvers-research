import pygame
from image_handler import get_player_sprite, get_background_image, get_mob_sprite

pygame.init()


# class Player(pygame.sprite.Sprite):
#    def __init__(self):
#       pygame.sprite.Sprite.__init__(self)
#        self.image = get_player_sprite()


def main():
    player_x = 400
    player_y = 570
    player_degree = 0
    mobs_x = [0, 600, 30]
    mobs_y = [350, 400, 450]
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Drunk Frogger")
    running = True

    while running:
        screen.blit(get_background_image(), (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        velocity = 3
        for i in range(len(mobs_x)):
            if i != 1:
                mobs_x[i] += velocity
                if mobs_x[i] == 720:
                    mobs_x[i] = 0
            else:
                mobs_x[i] -= velocity
                if mobs_x[i] == 0:
                    mobs_x[i] = 720
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > velocity:
            player_x -= velocity
            player_degree = 90
        if keys[pygame.K_RIGHT] and player_x < 800 - 40 - velocity:
            player_x += velocity
            player_degree = 270
        if keys[pygame.K_DOWN] and player_y < 600 - 30 - velocity:
            player_y += velocity
            player_degree = 180
        if keys[pygame.K_UP] and player_y > velocity:
            player_y -= velocity
            player_degree = 0
        if keys[pygame.K_ESCAPE]:
            running = False

        for i in range(len(mobs_x)):
            if i != 1:
                screen.blit(get_mob_sprite(False), (mobs_x[i], mobs_y[i]))
            else:
                screen.blit(get_mob_sprite(True), (mobs_x[i], mobs_y[i]))
        screen.blit(get_player_sprite(player_degree), (player_x, player_y))
        pygame.display.update()


if __name__ == '__main__':
    main()
