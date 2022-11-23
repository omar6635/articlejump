import pygame


class Text(pygame.sprite.Sprite):
    def __init__(self, text: str, color: tuple, size: int,  coordinates, font="Helvetica"):
        super(Text, self).__init__()
        pygame.font.init()
        # self.image = pygame.image.load()
        self.article_font = pygame.font.SysFont(font, size)
        self.article_surface = self.article_font.render(text, True, color)
        self.rect = self.article_surface.get_rect()
        self.rect.centerx = coordinates[0]
        self.rect.centery = coordinates[1]

    def draw_on_surface(self, screen, coordinates):
        screen.blit(self.article_surface, coordinates)
