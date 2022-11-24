# a&m's -> attributes and methods
import pygame
import database
import asyncio
import time
import math
from character import MainCharacter
from ground import Ground
from platforms import Platform
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
        self._ground = Ground((0, self._surface.get_height() - 50, 500, 100), "Der")
        # get a word-article combo from the database
        self._word_article_combo = database.get_random_word()
        # character attributes
        self._character = MainCharacter((window_width, window_height), self._ground.rect.y)
        self.user_initial_position = 204
        # result screen
        # also, the text displays "you win" by default. This is overwritten in the code for wrong answers.
        self._result_screen = ResultScreen("Correct!   ", (0, 255, 0))
        # create background list and variable for number of backgrounds required to fill screens
        self._background_list = []
        self._background_list.append(pygame.transform.scale(pygame.image.load("data/gfx/background_sprite2.png")
                                                            .convert(), (self._surface.get_width(), 150)))
        self._background_list.append(pygame.transform.scale(pygame.image.load("data/gfx/background_sprite3.png")
                                                            .convert(), (self._surface.get_width(), 150)))
        self.required_bgs = math.ceil(self._surface.get_height() / self._background_list[0].get_height()) + 2
        self.scroll = 0
        # platform attributes
        self._platform_one = Platform((0, 90), (107, 30), "der platform")
        self._platform_two = Platform((self._width/2-(107/2), 90), (107, 30), "das platform")
        self._platform_three = Platform((self._width-107, 90), (107, 30), "die platform")
        self._platform_group = pygame.sprite.Group(self._platform_one, self._platform_two, self._platform_three)
        for platform in self._platform_group:
            self._platform_group.add(platform.create_new_platform())
        # fonts
        self.main_font_30 = pygame.font.Font("data/fonts/Roboto_Condensed/RobotoCondensed-Bold.ttf", 30)
        self.main_font_50 = pygame.font.Font("data/fonts/Roboto_Condensed/RobotoCondensed-Bold.ttf", 50)
        self.main_font_20 = pygame.font.Font("data/fonts/Roboto_Condensed/RobotoCondensed-Bold.ttf", 20)
        # background gfx
        self.shadow = pygame.image.load("data/gfx/shadow.png")
        # formatting code
        self.format_panel_screen()
        self._result_list = [Platform((0, 0), (0, 0), "default")]
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
                clicked = False
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

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if self.allow_traversal() != "r border":
                self._character.rect.x += self._character.velocity
                if not self._character.jumping:
                    self._character.animation_mode = 1
                self._character.flip = False
        elif keys[pygame.K_LEFT]:
            if self.allow_traversal() != "l border":
                self._character.rect.x -= self._character.velocity
                if not self._character.jumping:
                    self._character.animation_mode = 1
                self._character.flip = True
        else:
            self._character.animation_mode = 0
        if keys[pygame.K_UP] and not self._character.jumping:
            self._character.on_platform = False
            self._character.jumping = True

    def allow_traversal(self) -> str:
        """
        allows for the user to go beyond the borders and pop out on the other side

        :return: String
        """
        if self._character.rect.x < -1 * self._character.rect.size[0]/2:
            self._character.rect.x = self._surface.get_width()-self._character.rect.size[0]/2
            return "l border"
        if self._character.rect.bottomright[0] > self._surface.get_width()+self._character.rect.size[0]/2:
            self._character.rect.x = -1 * self._character.rect.size[0]/2
            return "r border"
        # ensure that the character can not move past platform margins once on it
        """if self._on_platform:
            platform_to_check = self._result_list[0]
            if self._character.rect.bottomright[0] > platform_to_check.rect.topright[0]:
                return "r border"
            elif self._character.rect.bottomleft[0] < platform_to_check.rect.topleft[0]:
                return "l border"""

    def format_panel_screen(self):
        self._frame.set_caption("Artikeljump")
        self._frame.set_icon(self._character.image)

    def draw_surface_sprites(self):
        self._surface.fill((0, 0, 0))
        # blit the background(s) on the frame
        start_number = 150
        for i in range(0, self.required_bgs):
            self._surface.blit(self._background_list[i % 2], (0, start_number -
                                                              self.scroll))
            start_number -= 150
        # check if character's jumping or not
        if self._character.jumping:
            self._character.check_jump(self._character.jump_velocity)
            self._character.jump(self._ground.rect.y, self._platform_group)
        # draw the ground on background
        self._ground.blit_ground(self._surface, self.scroll)
        # draw the character on the background
        sprite_list = self._character.create_animation_list()
        self._character.animation(sprite_list, self._surface)
        # draw platforms on bg
        for platform in self._platform_group:
            platform.draw_platform(self._surface, self.scroll)
        # if self._draw_trail:
        #    line_trail = LineTrail(pygame.mouse.get_pos(), self, (self._character.rect.centerx,
        #                           self._surface.get_height() - self._character.rect.centery))
        #    line_trail.update(self._surface)
        # self.check_and_show_result(self._result_list[0].name, str.lower(self._word_article_combo[1]) + " platform")
        # make user fall of platform if not on it anymore
        if self._character.on_platform and not MainCharacter.check_character_platform_col(self._platform_group,
                                               self._character.rect.centerx, self._character.rect.bottom):
            self._character.jumping = True
            self._character.jump_velocity = 0
            self._character.on_platform = False
        # replace word under ground/platform and restart user position
        self.draw_next_frame()
        # scroll the background
        self.scroll_background()
        self._frame.update()

    def scroll_background(self):
        if self._character.jumping and self._character.jump_velocity > -20:
            self.scroll -= self._character.jump_velocity
            if abs(self.scroll) > self._surface.get_height():
                self.scroll = 0

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

    def check_and_show_result(self, on_platform, correct_result):
        if on_platform == correct_result:
            self._result_screen.change_text("Correct!", (0, 255, 0))
            self._result_screen.fade_in_out_effect()
            self._surface.blit(self._result_screen.textcop, (self._surface.get_rect().centerx -
                                                             self._result_screen.textcop.get_size()[0] / 2,
                                                             self._surface.get_rect().centery -
                                                             self._result_screen.textcop.get_size()[1] / 2))
        elif on_platform != "default" and on_platform != correct_result:
            self._result_screen.change_text("Incorrect!", (255, 0, 0))
            self._result_screen.fade_in_out_effect()
            self._surface.blit(self._result_screen.textcop, (self._surface.get_rect().centerx -
                                                             self._result_screen.textcop.get_size()[0] / 2,
                                                             self._surface.get_rect().centery -
                                                             self._result_screen.textcop.get_size()[1] / 2))

    def draw_next_frame(self):
        if self._result_screen.effect_finished:
            self._result_screen.upper_limit = False
            self._result_screen.effect_finished = False
            for platform in self._platform_group:
                if platform != self._result_list[0]:
                    self._platform_group.remove(platform)
            self._result_list = [Platform((0, 0), (0, 0), "default")]
            # FIXME: temporary fix for getting the same word as the current one. Solve in original class.
            current_word_article_combo = self._word_article_combo
            while current_word_article_combo[0] == self._word_article_combo[0]:
                self._word_article_combo = database.get_random_word()


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


class LineTrail(pygame.sprite.Sprite):
    def __init__(self, mouse_coords, parent, coordinates):
        super(LineTrail, self).__init__()
        self.mouse_coords = mouse_coords
        self.xpos = coordinates[0]
        self.ypos = coordinates[1]
        # self.rotate(coordinates[0], coordinates[1], width, height)
        self.parent = parent

    def update(self, parent):
        pygame.draw.line(parent, (0, 255, 0), (self.xpos, self.ypos), self.mouse_coords)

    """def rotate(self, pivot_x, pivot_y, width, height):
        if self.mouse_coords[0] < pivot_x and self.mouse_coords[1] > pivot_y:
            self.xpos, self.ypos = pivot_x - width, pivot_y
        elif self.mouse_coords[0] > pivot_x and self.mouse_coords[1] < pivot_y:
            self.xpos, self.ypos = pivot_x, pivot_y - height
        elif self.mouse_coords[0] < pivot_x and self.mouse_coords[1] < pivot_y:
            self.xpos, self.ypos = pivot_x - width, pivot_y - height
        elif self.mouse_coords[0] > pivot_x and self.mouse_coords[1] > pivot_y:
            self.xpos, self.ypos = pivot_x, pivot_y"""


async def main():
    main_frame = MainFrame(window_width=500, window_height=300)
    clock = pygame.time.Clock()
    while main_frame.running:
        clock.tick(60)
        main_frame.catch_events()
        if not main_frame.menu_running:
            main_frame.draw_surface_sprites()
            main_frame.handle_input()
        else:
            main_frame.create_draw_menu()
        await asyncio.sleep(0)

asyncio.run(main())
