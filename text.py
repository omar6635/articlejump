import pygame
import math
import time


class Text(pygame.sprite.Sprite):
    def __init__(self, text: str, color, size: int,  coordinates, font="Helvetica"):
        super(Text, self).__init__()
        pygame.font.init()
        # self.image = pygame.image.load()
        self.text = text
        self.color = color
        self.text_font = pygame.font.SysFont(font, size)
        self.text_surface = self.text_font.render(self.text, True, self.color)
        self.rect = self.text_surface.get_rect()
        self.rect.centerx = coordinates[0]
        self.rect.centery = coordinates[1]

    def draw_on_surface(self, screen: pygame.Surface, animate_text=False) -> None:
        if not animate_text:
            screen.blit(self.text_surface, self.rect)
        else:
            screen.blit(self.text_surface, (self.rect.x, self.rect.y + math.sin(time.time() * 5) * 5 - 25))

    def draw_on_surface_alpha(self, screen: pygame.Surface, alpha_val: int) -> None:
        textcop = self.text_surface.copy()
        alpha_surface = pygame.Surface(textcop.get_size(), pygame.SRCALPHA)
        alpha_surface.fill((255, 255, 255, alpha_val))
        textcop.blit(alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(textcop, self.rect)

    def scroll_text(self, scroll: int) -> None:
        self.rect.y += scroll

    def change_text(self, text):
        self.text_surface = self.text_font.render(text, True, self.color)

