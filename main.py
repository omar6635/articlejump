# a&m's -> attributes and methods
import pygame
import database
import time
import math
import copy
import random
from character import MainCharacter
from ground import Ground
from platforms import Platform
from result_screen import ResultScreen
from text import Text
from power_up import PowerUp
from load_sprite import load_sprite
from loading_bar import LoadingBar
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
        self._character = MainCharacter(self._ground.rect.midtop)
        # powerup attributes
        self.powerup = PowerUp((0, self._surface.get_width()), (0, self._character.rect.top))
        # UI elements
        self._wooden_frame = load_sprite(
            pygame.image.load("data/gfx/internet_asset_packs/dungeon pack/wooden_frame.png"),
            0, 0, 530, 174, 0.3, (0, 0, 0))
        self._whole_heart = load_sprite(pygame.image.load("data/gfx/internet_asset_packs/dungeonui.v1.png"),
                                        20, 133, 14, 15, 1.87, (0, 0, 0))
        self._half_heart = load_sprite(pygame.image.load("data/gfx/internet_asset_packs/dungeonui.v1.png"),
                                       35, 133, 14, 15, 1.87, (0, 0, 0))
        self._empty_heart = load_sprite(pygame.image.load("data/gfx/internet_asset_packs/dungeonui.v1.png"),
                                        52, 133, 14, 15, 1.87, (0, 0, 0))
        # dict of words drawn on screen
        self.word_article_dict = {}
        # list of word-article combos in tuples whose items only get popped in a game over condition
        self.word_article_list = []
        # result screen
        # also, the text displays "you win" by default. This is overwritten in the code for wrong answers.
        self._result_screen = ResultScreen("Correct!   ", (0, 255, 0))
        # create background list and variable for number of backgrounds required to fill screens
        self._background_list = []
        self._background_list.append(pygame.transform.scale(pygame.image.load("data/gfx/background_sprite2.png")
                                                            .convert(), (self._surface.get_width(),
                                                                         self._surface.get_height() / 2)))
        self._background_list.append(pygame.transform.scale(pygame.image.load("data/gfx/background_sprite3.png")
                                                            .convert(), (self._surface.get_width(),
                                                                         self._surface.get_height() / 2)))
        self.required_bgs = math.ceil(self._surface.get_height() / self._background_list[0].get_height()) + 2
        # platform attributes
        self.article_list = ["Der", "Die", "Das"]
        random.shuffle(self.article_list)
        self._platform_one = Platform((0, self._surface.get_height() - 220), (107, 30), self.article_list[0], False)
        self._platform_two = Platform((self._width / 2 - 107 / 2,
                                       self._surface.get_height() - 220), (107, 30), self.article_list[1], False)
        self._platform_three = Platform((self._width - 107, self._surface.get_height() - 220), (107, 30),
                                        self.article_list[2], False)
        self._platform_group = pygame.sprite.Group(self._platform_one, self._platform_two, self._platform_three)
        # for every 3 platforms in the platform group, blit a randomly generated word on the screen
        self.generate_draw_word(self._platform_group.sprites()[0].rect[0:2])
        self.max_platforms = 12
        # loading bar to serve as powerup timer
        self.loading_bar = LoadingBar(self._surface)
        self.loading_bar.rescale_lb(1.7)
        # fonts
        self.main_font = "data/fonts/Roboto_Condensed/RobotoCondensed-Regular.ttf"
        # background gfx
        self.shadow = pygame.image.load("data/gfx/shadow.png")
        # formatting code
        self.format_panel_screen()
        # game variables
        self.coins = 0
        self.stage = 0
        self.background_scroll = 0
        self.coin_multipler = 1
        self.lowest_word_rating = 0
        self.draw_powerup = False
        self.running = True
        self.menu_running = False
        self.gameover = False
        self.p_double_coins = False
        self.moving_platforms = False
        self.increase_rating = False
        # display splash and title screens
        # self.splash_screen()
        # self.title_screen()

    def catch_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not self.menu_running:
                    self.menu_running = True

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
            text_on_screen = Text("A Project by Omar, Ayberk and Michael", pygame.Color("#6A3940"), 30,
                                  self._surface.get_rect().center, self.main_font)
            text_on_screen.draw_on_surface(self._surface)
            pygame.display.update()
            pygame.time.delay(10)

    def title_screen(self):
        pygame.mixer.Sound.play(start_sfx)
        start_button = pygame.rect.Rect(self._surface.get_rect().centerx-50, self._surface.get_rect().centery+5, 100,
                                        46)
        display_ts = True
        logo = Text("ArtikelJump", pygame.Color("#6A3940"), 50, self._surface.get_rect().center)
        start_text = Text("START", (0, 0, 0), 20, start_button.center)
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
            logo.draw_on_surface(self._surface, True)
            pygame.draw.rect(self._surface, pygame.Color("#700e01"), start_button)
            start_text.draw_on_surface(self._surface)
            pygame.display.update()
            pygame.time.delay(10)

    def format_panel_screen(self):
        self._frame.set_caption("Artikeljump")
        self._frame.set_icon(self._character.image)

    def draw_update_surface_sprites(self):
        self._surface.fill((0, 0, 0))
        self.calc_stage()
        # move character
        scroll = self._character.move(self._ground.rect.y, self._platform_group, self._surface.get_rect()[2:],
                                      self.stage)
        # create background scroll by adding scroll onto it (cumulative variable)
        self.background_scroll += scroll
        if self.background_scroll > self._surface.get_height():
            self.background_scroll = 0
        # blit the background(s) on the frame
        start_number = self._surface.get_height() / 2
        for i in range(0, self.required_bgs):
            self._surface.blit(self._background_list[i % 2], (0, start_number +
                                                              self.background_scroll))
            start_number -= self._surface.get_height() / 2
        # draw the ground on background
        self._ground.blit_ground(self._surface, scroll)
        # draw the character on the background
        sprite_list = self._character.create_animation_list()
        self._character.animation(sprite_list, self._surface)
        # create platforms if current amount is below limit
        while len(self._platform_group.sprites()) < self.max_platforms:
            move = False
            if self.moving_platforms:
                # 1 in 5 chance that a platform is moving
                moving_chance = random.randint(1, 5)
                if moving_chance == 2:
                    move = True
            buffer_list = []
            random.shuffle(self.article_list)
            for i in range(-3, 0, 1):
                buffer_list.append(self._platform_group.sprites()[i].create_new_platforms(self.article_list[i], move))
            self.generate_draw_word(buffer_list[0].rect[0:2])
            self._platform_group.add(buffer_list)
        # draw platforms on bg
        for platform in self._platform_group:
            platform.update(scroll, self._surface.get_size(), self.word_article_dict)
            platform.draw_platform(self._surface)
        # draw words on bg
        for sub_list in list(self.word_article_dict.items()):
            sub_list[0].scroll_text(scroll)
            sub_list[0].draw_on_surface_alpha(self._surface, 75)
        # draw UI elements
        # coins UI elements
        self._surface.blit(self._wooden_frame, (-30, -14))
        self.draw_score()
        # heart UI elements
        self._surface.blit(self._wooden_frame, (370, -14))
        self.draw_hearts()
        # check if gameover condition is met
        if self.gameover_check():
            self.gameover = True
        # check if user has made correct decision
        if self._character.on_platform != "":
            self.check_answer()
            self._character.on_platform = ""
        # powerup 1
        # make it so that there's a 1 in 1000 chance a powerup spawns
        if not self.p_double_coins:
            self.assess_draw_powerup()
        # if draw_powerup evaluates to true, draw powerup
        if self.draw_powerup:
            self.powerup.draw_on_screen(self._surface)
            self.powerup.update(scroll)
            self.p_double_coins = self._character.check_power_up_collision(self.powerup)
            if self.p_double_coins:
                self.powerup.reposition_powerup()
                self.powerup.timer_started = False
                self.draw_powerup = False
                # FIXME: use this for the progress bar
                self.powerup.last_time = pygame.time.get_ticks()
            if self.powerup.draw_timer():
                self.draw_powerup = False
        # if user collected the powerup and it's still in effect, double the amount of coins earned
        if self.p_double_coins:
            self.coin_multipler = 2
            # blit loading bar
            self.loading_bar.resize_bar(self.powerup.last_time)
            self.loading_bar.draw_on_screen()
            if self.powerup.effect_timer():
                self.p_double_coins = False
                self.coin_multipler = 1
                self.loading_bar.bar_obj_list.clear()
        # as user progresses, make the game harder by choosing harder words and making the game more dynamic
        self.raise_difficulty()
        # if timer_started runs out, delete powerup.
        self._frame.update()

    def draw_score(self):
        coin_sprite = load_sprite(pygame.image.load("data/gfx/internet_asset_packs/coins/coin2_20x20.png"),
                                  0, 0, 22, 20, 1.2, (0, 0, 0))
        self._surface.blit(coin_sprite, (0, 0))
        score_text = Text(" " + str(self.coins), (0, 0, 0), 25, (0, 0), self.main_font)
        score_text.rect.topleft = (25, 5)
        score_text.draw_on_surface(self._surface)

    def raise_difficulty(self):
        if self.coins > 2000:
            self.moving_platforms = True

        if self.coins % 1000 == 0 and self.increase_rating:
            self.lowest_word_rating += 1
            print("word rating increased")
            self.increase_rating = False

        if self.coins % 1000 != 0:
            self.increase_rating = True

    def draw_hearts(self):
        whole_hearts = self._character.lives
        empty_hearts = 3 - self._character.lives
        first_x_coord = 390
        x_coord_increment = 40
        for i in range(whole_hearts):
            self._surface.blit(self._whole_heart, (first_x_coord, -2))
            first_x_coord += x_coord_increment
        for i in range(empty_hearts):
            self._surface.blit(self._empty_heart, (first_x_coord, -2))
            first_x_coord += x_coord_increment

    def assess_draw_powerup(self) -> None:
        rand_number = random.randrange(0, 10)
        if rand_number == 5:
            self.draw_powerup = True

    def gameover_check(self):
        if self._character.rect.top > self._surface.get_height():
            if self._character.lives > 0:
                self._character.lives -= 1
                self._character.rect.midbottom = self._character.last_saved_pos
            else:
                return True

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
                if event.type == pygame.QUIT:
                    self.running = False
                    self.menu_running = False

    def check_answer(self):
        # check what stage the user is at to make sure the guess is being made for the right word
        if self.word_article_list[self.stage][1] == self._character.on_platform:
            self.coins += 50 * self.coin_multipler

    def calc_stage(self):
        real_scroll = self._ground.rect.y - 766
        self.stage = real_scroll // 200 + 1

    def generate_draw_word(self, coordinates: tuple) -> None:
        # prepare coordinates
        a_y = copy.deepcopy(coordinates[1]) - 90
        a_x = copy.deepcopy(coordinates[0]) + self._surface.get_width() / 2
        # get a word-article combo from the database
        word_article_combo = database.get_random_word()
        # as long as the database returns a duplicate, get another one
        while word_article_combo[0] in [i[0].text for i in list(self.word_article_dict.items())] and \
                self.lowest_word_rating < word_article_combo[2]:
            word_article_combo = database.get_random_word()
        # create a Text object
        text_obj = Text(word_article_combo[0], (0, 0, 0), 40, (a_x, a_y))
        # add the Text object and its correct article to dict
        self.word_article_dict[text_obj] = word_article_combo[1]
        self.word_article_list.append(word_article_combo)

    def reset_game_variables(self) -> None:
        self.gameover = False
        self.coins = 0
        self.background_scroll = 0
        self.stage = 0
        self._character.platform_stage = -1
        self._character.on_platform = ""
        # reset character, ground and platform positions
        self._character.lives = 3
        self._ground.rect.x = 0
        self._ground.rect.y = self._surface.get_size()[1]-50
        self._character.jumping = False
        self._character.rect.midbottom = self._ground.rect.midtop
        self._platform_group.empty()
        random.shuffle(self.article_list)
        self._platform_one = Platform((0, self._surface.get_height() - 220), (107, 30), self.article_list[0], False)
        self._platform_two = Platform((self._width / 2 - 107 / 2,
                                       self._surface.get_height() - 220), (107, 30), self.article_list[1], False)
        self._platform_three = Platform((self._width - 107, self._surface.get_height() - 220), (107, 30),
                                        self.article_list[2], False)
        self._platform_group.add(self._platform_one, self._platform_two, self._platform_three)
        self.word_article_dict = {}
        self.word_article_list = []
        self.generate_draw_word(self._platform_group.sprites()[0].rect[0:2])

    # getter and setter decorators
    @property
    def surface(self):
        return self._surface

    @property
    def frame(self):
        return self._frame


def draw_game_over_text(main_frame):
    game_over_text = Text("GAME OVER", (255, 255, 255), 50,
                          (main_frame.surface.get_rect().centerx, main_frame.surface.get_rect().centery - 50),
                          main_frame.main_font)
    score_text = Text("SCORE: " + "50", (255, 255, 255), 50,
                      (main_frame.surface.get_rect().centerx, main_frame.surface.get_rect().centery),
                      main_frame.main_font)
    play_again_text = Text("PRESS SPACE TO RESTART", (255, 255, 255), 50,
                           (main_frame.surface.get_rect().centerx, main_frame.surface.get_rect().centery + 50),
                           main_frame.main_font)
    game_over_text.draw_on_surface(main_frame.surface)
    score_text.draw_on_surface(main_frame.surface)
    play_again_text.draw_on_surface(main_frame.surface)


if __name__ == "__main__":
    game_window = MainFrame(window_width=500, window_height=700)
    clock = pygame.time.Clock()
    update_frame = True
    while game_window.running:
        clock.tick(60)
        game_window.catch_events()
        if not game_window.menu_running:
            if not game_window.gameover:
                game_window.draw_update_surface_sprites()
            else:
                draw_game_over_text(game_window)
                if update_frame:
                    game_window.frame.update()
                    update_frame = False
                key = pygame.key.get_pressed()
                if key[pygame.K_SPACE]:
                    update_frame = True
                    game_window.reset_game_variables()
        else:
            game_window.create_draw_menu()
