import pygame


def load_sprite(sprite, x, y, width, height, scale, color):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sprite, (0, 0), (x, y, width, height))
    # resize image
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(color)
    return image
