import pygame


class Ground(pygame.sprite.Sprite):
    def __init__(self, coords_and_dimensions: tuple):
        super(Ground, self).__init__()
        self.image = pygame.image.load("data/gfx/ground_sprite.png").convert_alpha()
        # self.image = pygame.transform.scale(self.image, (self.image.get_width()*3, self.image.get_height()*3))
        self.rect = pygame.rect.Rect(coords_and_dimensions[0], coords_and_dimensions[1], coords_and_dimensions[2],
                                     coords_and_dimensions[3])

    def blit_ground(self, surface, scroll):
        self.rect.y += scroll
        pygame.draw.rect(surface, (0, 255, 0), self.rect)


if __name__ == "__main__":
    pygame.init()
    display = pygame.display.set_mode((500, 500))
    my_ground = Ground((0, 400))
    run = True
    while run:
        display.fill((55, 55, 55))
        display.blit(my_ground.image, (0, 300))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
    pygame.quit()
