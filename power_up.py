import pygame
import random
from load_sprite import load_sprite


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x_range, y_range):
        super(PowerUp, self).__init__()
        self.image = load_sprite(pygame.image.load("data/gfx/internet_asset_packs/coins/coin3_20x20.png"),
                                 0, 0, 22, 20, 2, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.x_range = x_range
        self.y_range = y_range
        self.rect.centerx = random.randrange(x_range[0], x_range[1]-self.rect.size[0])
        self.rect.centery = random.randrange(*y_range)
        self.last_time_draw = 0
        self.last_time_effect = 0
        self.disappear = 2000
        self.effect = 2000
        self.timer_started = False

    def draw_on_screen(self, screen):
        if not self.timer_started:
            self.last_time_draw = pygame.time.get_ticks()
            self.timer_started = True
        screen.blit(self.image, self.rect)

    def update(self, scroll):
        self.rect.y += scroll

    def draw_timer(self, pause_timer) -> True:
        current_time = pygame.time.get_ticks()
        time_delta = current_time - self.last_time_draw - pause_timer
        if time_delta >= self.disappear:
            self.reposition_powerup()
            self.timer_started = False
            self.last_time_draw = 0
            return True

    def effect_timer(self, pause_duration):
        current_time = pygame.time.get_ticks()
        time_delta = current_time - self.last_time_effect - pause_duration
        if time_delta >= self.effect:
            self.last_time_effect = 0
            return True

    def reposition_powerup(self):
        self.rect.centerx = random.randrange(self.x_range[0], self.x_range[1] - self.rect.size[0])
        self.rect.centery = random.randrange(*self.y_range)


if __name__ == "__main__":
    pygame.init()
    display = pygame.display.set_mode((500, 500))
    power_up = PowerUp((0, 500), (0, 400))
    run = True
    while run:
        display.fill((55, 55, 55))
        power_up.draw_on_screen(display)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
    pygame.quit()