import pygame


class ResultScreen:
    def __init__(self, text: str, color: tuple):
        super(ResultScreen, self).__init__()
        pygame.font.init()
        self.font = pygame.font.SysFont("Calibri", 50)
        self.textsurface = self.font.render(text, True, color)
        self.textcop = self.textsurface.copy()
        self.alphasurf = pygame.Surface(self.textcop.get_size(), pygame.SRCALPHA)
        self.alphaval = 0
        self.upper_limit = False
        self.effect_finished = False

    def fade_in_out_effect(self):
        # to be used later for displaying win or loss text
        # this code can produce a fade in or fade out effect alike
        # alphaval cannot reach 0. otherwise, unwanted effects can occur
        if not self.upper_limit:
            self.alphaval = min(self.alphaval + 4, 255)
        else:
            self.alphaval = max(self.alphaval-4, 0)
        # using a copy of the original text makes things noticeably faster
        self.textcop = self.textsurface.copy()
        # fill alphasurface with a certain opacity of white (lower alpha = more transparent)
        self.alphasurf.fill((255, 255, 255, self.alphaval))
        # blend white surface onto text to change its opacity
        self.textcop.blit(self.alphasurf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        if self.alphaval == 255:
            self.upper_limit = True
        if self.alphaval == 0:
            self.effect_finished = True

    def change_text(self, new_text: str, color):
        self.textsurface = self.font.render(new_text, True, color)
