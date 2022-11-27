# a&m's -> attributes and methods
import pygame
import database
import asyncio
import time
import math
import copy
from character import MainCharacter
from ground import Ground
from platforms import Platform
from result_screen import ResultScreen
from text import Text
# initialize pygame globally for global variables
pygame.init()
# database object is defined globally so that any class can access it
database = database.SQLMain()
# sfx
jump_sfx = pygame.mixer.Sound("data/sfx/jump2.mp3")
dead_sfx = pygame.mixer.Sound("data/sfx/dead.wav")
coin_collect_sfx = pygame.mixer.Sound("data/sfx/coin collect.wav")
explosion_sfx = pygame.mixer.Sound("data/sfx/explosion.wav")
power_up_sfx = pygame.mixer.Sound("data/sfx/power_up.wav")
start_sfx = pygame.mixer.Sound("data/sfx/start.mp3")


class MainFrame:
    def __init__(self, window_width, window_height):
        # display attributes
        self._width, self._height = window_width, window_height
        self._frame = pygame.display
        self._surface = self._frame.set_mode((self._width, self._height))
        # create ground platform
        self._ground = Ground((0, self._surface.get_height() - 50, 500, 100))
        # character attributes
        self._character = MainCharacter((window_width, window_height), self._ground.rect.y)
        # list of words drawn on screen
        self.word_article_dict = {}
        # result screen
        # also, the text displays "you win" by default. This is overwritten in the code for wrong answers.
        self._result_screen = ResultScreen("Correct!   ", (0, 255, 0))
        # create background list and variable for number of backgrounds required to fill screens
        self._background_list = []
        self._background_list.append(pygame.transform.scale(pygame.image.load("data/gfx/background_sprite2.png")
                                                            .convert(), (self._surface.get_width(),
                                                                         self._surface.get_height()/2)))
        self._background_list.append(pygame.transform.scale(pygame.image.load("data/gfx/background_sprite3.png")
                                                            .convert(), (self._surface.get_width(),
                                                                         self._surface.get_height()/2)))
        self.required_bgs = math.ceil(self._surface.get_height() / self._background_list[0].get_height()) + 2
        # platform attributes
        self._platform_one = Platform((0, self._surface.get_height()-220), (107, 30), "der platform")
        self._platform_two = Platform((self._width/2-107/2,
                                       self._surface.get_height()-220), (107, 30), "das platform")
        self._platform_three = Platform((self._width-107, self._surface.get_height()-220), (107, 30), "die platform")
        self._platform_group = pygame.sprite.Group(self._platform_one, self._platform_two, self._platform_three)
        # for every 3 platforms in the platform group, blit a randomly generated word on the screen
        self.generate_draw_word(self._platform_group.sprites()[0].rect[0:2])
        self.max_platforms = 9
        # fonts
        self.main_font_30 = pygame.font.Font("data/fonts/Roboto_Condensed/RobotoCondensed-Bold.ttf", 30)
        self.main_font_50 = pygame.font.Font("data/fonts/Roboto_Condensed/RobotoCondensed-Bold.ttf", 50)
        self.main_font_20 = pygame.font.Font("data/fonts/Roboto_Condensed/RobotoCondensed-Bold.ttf", 20)
        # background gfx
        self.shadow = pygame.image.load("data/gfx/shadow.png")
        # formatting code
        self.format_panel_screen()
        self._result_list = [Platform((0, 0), (0, 0), "default")]
        self.background_scroll = 0
        self._force_descent = False
        self._draw_trail = False
        self.running = True
        self.menu_running = False
        # display splash and title screens
        # self.splash_screen()
        # self.title_screen()

    def catch_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not self.menu_running:
                    self.menu_running = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._draw_trail = not self._draw_trail

    def splash_screen(self):
        pygame.mixer.Sound.play(start_sfx)
        previous_time = time.time()
        splash_screen_timer = 0
        while splash_screen_timer < 100:
            current_time = time.time() - previous_time
            current_time *= 60
            previous_time = time.time()
            splash_screen_timer += current_time
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            # fill the background with teal (a shade of blue)
            self._surface.fill((0, 128, 128))
            text_on_screen = self.main_font_30.render("A Project by Omar, Ayberk and Michael", True,
                                                      pygame.Color("#6A3940"))
            self._surface.blit(text_on_screen, (self._surface.get_width()/2 - text_on_screen.get_width()/2,
                                                self._surface.get_height()/2 - text_on_screen.get_height()/2))
            pygame.display.update()
            pygame.time.delay(10)

    def title_screen(self):
        pygame.mixer.Sound.play(start_sfx)
        start_button = pygame.rect.Rect(self._surface.get_width()/2-50, 160, 100, 46)
        display_ts = True
        logo = self.main_font_50.render("AritkelJump", True, pygame.Color("#6A3940"))
        start_text = self.main_font_20.render("START", True, (0, 0, 0))
        while display_ts:
            mouse_coords = pygame.mouse.get_pos()
            clicked = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    clicked = True
                if event.type == pygame.QUIT:
                    pygame.quit()
            if clicked and start_button.collidepoint(mouse_coords):
                pygame.mixer.Sound.play(jump_sfx)
                display_ts = False
            self._surface.fill((0, 128, 128))
            self._surface.blit(self.shadow, (0, 0))
            self._surface.blit(logo, (self._surface.get_width()/2 - logo.get_width()/2,
                                      self._surface.get_height()/2 - logo.get_height()/2 +
                                      math.sin(time.time()*5)*5 - 25))
            pygame.draw.rect(self._surface, pygame.Color("#700e01"), start_button)
            self._surface.blit(start_text, (start_button.x+start_text.get_width()/2-5,
                                            start_button.y+start_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(10)

    def format_panel_screen(self):
        self._frame.set_caption("Artikeljump")
        self._frame.set_icon(self._character.image)

    def draw_update_surface_sprites(self):
        self._surface.fill((0, 0, 0))
        # move character
        scroll = self._character.move(self._ground.rect.y, self._platform_group, self._surface.get_rect()[2:])
        # create background scroll by adding scroll onto it (cumulative variable)
        self.background_scroll += scroll
        if self.background_scroll > self._surface.get_height():
            self.background_scroll = 0
        # blit the background(s) on the frame
        start_number = self._surface.get_height()/2
        for i in range(0, self.required_bgs):
            self._surface.blit(self._background_list[i % 2], (0, start_number +
                                                              self.background_scroll))
            start_number -= self._surface.get_height()/2

        # draw the ground on background
        self._ground.blit_ground(self._surface, scroll)
        # draw the character on the background
        sprite_list = self._character.create_animation_list()
        self._character.animation(sprite_list, self._surface)
        # create platforms if current amount is below limit
        while len(self._platform_group.sprites()) < self.max_platforms:
            buffer_list = []
            for i in range(-3, 0, 1):
                buffer_list.append(self._platform_group.sprites()[i].create_new_platforms())
            self.generate_draw_word(buffer_list[0].rect[0:2])
            self._platform_group.add(buffer_list)
        # draw platforms on bg
        for platform in self._platform_group:
            platform.update(scroll, self._surface.get_height(), self.word_article_dict)
            platform.draw_platform(self._surface)
        # draw words on bg
        for sub_list in list(self.word_article_dict.items()):
            sub_list[0].scroll_text(scroll)
            sub_list[0].draw_on_surface_alpha(self._surface, 75)
        # background_scroll the background
        self._frame.update()

    def create_draw_menu(self):
        while self.menu_running:
            resume_button = pygame.Rect(50, 5, 150, 50)
            exit_button = pygame.Rect(50, 105, 150, 50)
            pygame.font.init()
            font = pygame.font.SysFont("Helvetica", 40)
            text_exit = font.render("Exit", True, (0, 225, 255))
            text_resume = font.render("Resume", True, (0, 255, 255))
            textrect_exit = text_exit.get_rect()
            textrect_exit.center = (125, 127)
            textrect_resume = text_resume.get_rect()
            textrect_resume.center = (125, 27)
            self._surface.fill((0, 0, 0))
            pygame.draw.rect(self._surface, (255, 0, 0), exit_button)
            pygame.draw.rect(self._surface, (255, 0, 0), resume_button)
            self._surface.blit(text_exit, textrect_exit)
            self._surface.blit(text_resume, textrect_resume)
            self._frame.flip()
            for event in pygame.event.get():
                cursor_pos = pygame.mouse.get_pos()
                if resume_button.collidepoint(cursor_pos):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.menu_running = False
                if exit_button.collidepoint(cursor_pos):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.running = False
                        self.menu_running = False
                        pygame.quit()
                if event.type == pygame.QUIT:
                    self.running = False
                    self.menu_running = False
                    pygame.quit()

    def generate_draw_word(self, coordinates: tuple) -> None:
        # prepare coordinates
        a_y = copy.deepcopy(coordinates[1]) - 90
        a_x = copy.deepcopy(coordinates[0]) + self._surface.get_width()/2
        # get a word-article combo from the database
        word_article_combo = database.get_random_word()
        # as long as the database returns a duplicate, get another one
        while word_article_combo[0] in [i[0].text for i in list(self.word_article_dict.items())]:
            word_article_combo = database.get_random_word()
        # create a Text object
        text_obj = Text(word_article_combo[0], (0, 0, 0), 40, (a_x, a_y))
        # add the Text object and its correct article to dict
        self.word_article_dict[text_obj] = word_article_combo[1]


async def main():
    main_frame = MainFrame(window_width=500, window_height=700)
    clock = pygame.time.Clock()
    while main_frame.running:
        clock.tick(60)
        main_frame.catch_events()
        if not main_frame.menu_running:
            main_frame.draw_update_surface_sprites()
        else:
            main_frame.create_draw_menu()
        await asyncio.sleep(0)

asyncio.run(main())
