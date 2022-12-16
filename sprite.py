import pygame
from abc import ABC


class Sprite(ABC, pygame.sprite.Sprite):
    """
    Abstract sprite class to be implemented by all sprites.
    """
    def __init__(self):
        super(Sprite, self).__init__()

    def draw_on_screen(self, screen):
        screen.blit(self.image, self.rect)
