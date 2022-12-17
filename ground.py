import pygame
from game_functions import load_sprite
from sprite import Sprite


class Ground(Sprite):
    def __init__(self, coords: tuple):
        super(Ground, self).__init__()
        self.image = load_sprite(pygame.image.load("data/gfx/ground_sprite.png"), 0, 68,
                                 128, 30, 4, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = coords

    def blit_ground(self, surface, scroll):
        self.rect.y += scroll
        surface.blit(self.image, self.rect)


if __name__ == "__main__":
    pygame.init()
    display = pygame.display.set_mode((500, 500))
    my_ground = Ground((0, 400))
    run = True
    while run:
        display.fill((55, 55, 55))
        pygame.draw.rect(display, (255, 255, 255), my_ground.rect, 1)
        my_ground.blit_ground(display, 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
    pygame.quit()
