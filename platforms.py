from __future__ import annotations
import pygame
from text import Text


class Platform(pygame.sprite.Sprite):
    def __init__(self, coordinates, dimesions, name):
        # calling parent class constructor in order to get access to its a&m's
        super(Platform, self).__init__()
        self.name = name
        self.image = pygame.transform.scale(pygame.image.load("data/gfx/platform_sprite.png"), dimesions)
        self.rect = self.image.get_rect()
        self.coordinates = coordinates
        self.rect.topleft = self.coordinates
        self.article = Text(str.upper(name[0:3]), (0, 0, 0), 40, (self.rect.centerx,
                                                                  self.rect.centery + self.rect.size[1] - 7))

    def update(self, scroll: int, screen_height: int, word_dict: dict) -> None:
        self.rect.y += scroll
        self.article.rect.y += scroll
        if self.rect.top > screen_height:
            self.kill()
            if self.rect.x == 393:
                key_list = [i[0] for i in list(word_dict.items())]
                word_dict.pop(key_list[0])

    def draw_platform(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.article.article_surface, self.article.rect)

    def create_new_platforms(self, article: str) -> Platform:
        new_y = self.rect.y - 200
        new_platform_obj = Platform((self.coordinates[0], new_y), self.rect.size, article)
        return new_platform_obj


if __name__ == "__main__":
    pygame.init()
    display = pygame.display.set_mode((500, 1000))
    my_platform = Platform((250, 750), (107, 30), "Der")
    new_platform = my_platform.create_new_platforms()
    run = True
    while run:
        display.fill((55, 55, 55))
        display.blit(my_platform.image, my_platform.rect)
        display.blit(new_platform.image, new_platform.rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
    pygame.quit()
