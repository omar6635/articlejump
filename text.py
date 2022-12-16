import pygame
import math
import time


class Text(pygame.sprite.Sprite):
    def __init__(self, text: str, color, size: int,  coordinates, font="Helvetica", set_midleft=False):
        super(Text, self).__init__()
        pygame.font.init()
        # self.image = pygame.image.load()
        self.text = text
        self.color = color
        self.text_font = pygame.font.SysFont(font, size)
        self.text_surface = self.text_font.render(self.text, True, self.color)
        self.rect = self.text_surface.get_rect()
        if set_midleft:
            self.rect.midleft = coordinates
        else:
            self.rect.center = coordinates

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

    def draw_multiline_text(self, screen: pygame.Surface, coords, line_list) -> None:
        space = self.text_font.size(" ")[0]
        x, y = coords
        word_width, word_height = (0, 0)
        for lines in line_list:
            for word in lines:
                word_surface = self.text_font.render(word, True, self.color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= screen.get_width():
                    x = coords[0]
                    y += word_height + 3
                screen.blit(word_surface, (x, y))
                x += word_width + space
            x = coords[0]
            y += word_height + 3

    def scroll_text(self, scroll: int) -> None:
        self.rect.y += scroll

    def change_text(self, text):
        self.text_surface = self.text_font.render(text, True, self.color)


if __name__ == "__main__":
    pygame.init()
    display = pygame.display.set_mode((500, 500))
    my_char = Text("Mah", (0, 0, 0), 18, (0, 100), set_midleft=True)
    string_to_draw = "Hello Everyone! \nWe are trying to display text on a pygame window"
    run = True
    while run:
        display.fill((255, 255, 255))
        my_char.draw_multiline_text(display, (0, 0), string_to_draw)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
    pygame.quit()
