import pygame


class Text(pygame.sprite.Sprite):
    def __init__(self, text: str, color: tuple, size: int,  coordinates, font="Helvetica"):
        super(Text, self).__init__()
        pygame.font.init()
        # self.image = pygame.image.load()
        self.text = text
        self.article_font = pygame.font.SysFont(font, size)
        self.article_surface = self.article_font.render(self.text, True, color)
        self.rect = self.article_surface.get_rect()
        self.rect.centerx = coordinates[0]
        self.rect.centery = coordinates[1]

    def draw_on_surface(self, screen: pygame.Surface) -> None:
        screen.blit(self.article_surface, self.rect)

    def draw_on_surface_alpha(self, screen: pygame.Surface, alpha_val: int) -> None:
        textcop = self.article_surface.copy()
        alpha_surface = pygame.Surface(textcop.get_size(), pygame.SRCALPHA)
        alpha_surface.fill((255, 255, 255, alpha_val))
        textcop.blit(alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(textcop, self.rect)

    def scroll_text(self, scroll: int) -> None:
        self.rect.y += scroll
