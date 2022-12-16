import pygame
from game_bonuses import GameBonuses


class PowerUp(GameBonuses):
    def __init__(self, x_range, y_range, image):
        super(PowerUp, self).__init__(x_range, y_range, image)
        self.sfx = pygame.mixer.Sound("data/sfx/coin collect.wav")

    def draw_on_screen(self, surface, scroll, character):
        # if draw_powerup evaluates to true, draw powerup
        if not self.timer_started:
            self.last_time_draw = pygame.time.get_ticks()
            self.timer_started = True
        surface.blit(self.image, self.rect)
        self.update(scroll)
        self.power_up_active = character.check_power_up_collision(self)
        if self.power_up_active:
            self.reposition_powerup()
            self.draw_powerup = False
            self.last_time_effect = pygame.time.get_ticks()
            self.sfx.play()
        elif self.draw_timer():
            self.draw_powerup = False
            self.pause_duration_draw = 0

