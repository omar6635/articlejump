import pygame


def load_sprite(sprite, frame, width, height, scale, color, specify_manually=False, x=0, y=0):
    image = pygame.Surface((width, height)).convert_alpha()
    if not specify_manually:
        image.blit(sprite, (0, 0), (frame * width, 0, width, height))
    elif specify_manually:
        image.blit(sprite, (0, 0), (x, y, width, height))
    # resize image
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(color)
    return image
