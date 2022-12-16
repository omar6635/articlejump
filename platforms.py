from __future__ import annotations
import pygame
import random
from load_sprite import load_sprite
from text import Text


class Platform(pygame.sprite.Sprite):
    def __init__(self, coordinates, name, moving_platform):
        # calling parent class constructor in order to get access to its a&m's
        super(Platform, self).__init__()
        self.name = name
        self.image = load_sprite(pygame.image.load("data/gfx/platform_sprite.png"), 6, 6, 201, 30, 0.58,
                                 (0, 0, 0))
        self.rect = self.image.get_rect()
        self.coordinates = coordinates
        self.rect.center = self.coordinates
        self.article = Text(str.upper(name[0:3]), pygame.Color("#3F301D"), 40, (self.rect.midbottom[0],
                                                                                self.rect.midbottom[1]+13))
        self.moving = moving_platform
        self.move_direction = random.choice([1, -1])
        self.move_space = 20
        self.move_speed = random.randint(1, 2)

    def update(self, scroll: int, screen_dimensions: tuple, word_dict: dict) -> None:
        # move platform if of moving type
        if self.moving:
            self.move_space += 1
            self.rect.x += self.move_direction * self.move_speed
            self.article.rect.x += self.move_direction * self.move_speed

        if self.move_space > 40 or self.rect.left < 0 or self.rect.right > screen_dimensions[0]:
            self.move_direction *= -1
            self.move_space = 0

        self.rect.y += scroll
        self.article.rect.y += scroll
        if self.rect.top > screen_dimensions[1]:
            self.kill()
            if 400 < self.rect.right <= screen_dimensions[0]:
                key_list = [i[0] for i in list(word_dict.items())]
                word_dict.pop(key_list[0])

    def draw_platform(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.article.text_surface, self.article.rect)

    def create_new_platforms(self, article: str, moving: bool) -> Platform:
        new_y = self.rect.y - 200
        new_platform_obj = Platform((self.coordinates[0], new_y), article, moving)
        return new_platform_obj


if __name__ == "__main__":
    pygame.init()
    display = pygame.display.set_mode((500, 1000))
    my_platform = Platform((250, 750), "Der", False)
    new_platform = my_platform.create_new_platforms("Der", False)
    run = True
    while run:
        display.fill(pygame.Color("#73c2fb"))
        my_platform.draw_platform(display)
        new_platform.draw_platform(display)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
    pygame.quit()
