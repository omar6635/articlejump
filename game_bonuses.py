import pygame
import random
from game_functions import load_sprite
from abc import ABC


class GameBonuses(ABC, pygame.sprite.Sprite):
    def __init__(self, x_range, y_range, image):
        super(GameBonuses, self).__init__()
        self.image = load_sprite(pygame.image.load(image), 0, 0, 22, 20, 2, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.x_range = x_range
        self.y_range = y_range
        self.rect.centerx = random.randrange(x_range[0], x_range[1] - self.rect.size[0])
        self.rect.centery = random.randrange(*y_range)
        self.last_time_draw = 0
        self.last_time_effect = 0
        self.disappear = 2000
        self.effect = 2000
        self.pause_duration_draw = 0
        self.pause_duration_effect = 0
        self.timer_started = False
        self.draw_powerup = False
        self.power_up_active = False

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
        elif self.draw_timer():
            self.draw_powerup = False
            self.pause_duration_draw = 0

    def update(self, scroll):
        self.rect.y += scroll

    def draw_timer(self) -> bool:
        current_time = pygame.time.get_ticks()
        time_delta = current_time - self.last_time_draw - self.pause_duration_draw
        if time_delta >= self.disappear:
            self.reposition_powerup()
            self.last_time_draw = 0
            self.timer_started = False
            return True

    def effect_timer(self):
        current_time = pygame.time.get_ticks()
        time_delta = current_time - self.last_time_effect - self.pause_duration_effect
        if time_delta >= self.effect:
            self.last_time_effect = 0
            self.pause_duration_effect = 0
            self.timer_started = False
            return True

    def reposition_powerup(self):
        self.rect.centerx = random.randrange(self.x_range[0], self.x_range[1] - self.rect.size[0])
        self.rect.centery = random.randrange(*self.y_range)

    def assess_draw_powerup(self) -> None:
        rand_number = random.randrange(0, 500)
        if rand_number == 5:
            if not self.power_up_active:
                self.draw_powerup = True
