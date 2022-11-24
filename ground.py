import pygame
import copy
from text import Text


class Ground(pygame.sprite.Sprite):
    def __init__(self, coords_and_dimensions: tuple, word: str):
        super(Ground, self).__init__()
        self.image = pygame.image.load("data/gfx/ground_sprite.png").convert_alpha()
        #self.image = pygame.transform.scale(self.image, (self.image.get_width()*3, self.image.get_height()*3))
        self.rect = pygame.rect.Rect(coords_and_dimensions[0], coords_and_dimensions[1], coords_and_dimensions[2],
                                     coords_and_dimensions[3])
        self.rect_deepcopy = copy.deepcopy(self.rect.y)
        self.word = Text(word, (0, 0, 0), 60, (self.rect.centerx, self.rect.centery-17))
        self.word_y_deepcopy = copy.deepcopy(self.word.rect.y)

    def blit_ground(self, surface, scroll):
        self.rect.y = self.rect_deepcopy - scroll
        self.word.rect.y = self.word_y_deepcopy - scroll
        pygame.draw.rect(surface, (0, 255, 0), (self.rect.x, self.rect.y-scroll, self.rect.size[0], self.rect.size[1]))
        surface.blit(self.word.article_surface, (self.word.rect.x, self.word.rect.y-scroll))

    def change_word(self, new_word):
        self.word = Text(new_word, (0, 0, 0), 60, (self.rect.centerx, self.rect.centery-17))


if __name__ == "__main__":
    pygame.init()
    display = pygame.display.set_mode((500, 500))
    my_ground = Ground((0, 400), "Der")
    run = True
    while run:
        display.fill((55, 55, 55))
        display.blit(my_ground.image, (0, 300))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
    pygame.quit()
