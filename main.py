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
from button import Button
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
        self._ground = Ground((0, self._surface.get_height() - 100))
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
        self._platform_one = Platform((0, self._surface.get_height() - 270), (107, 30), self.article_list[0], False)
        self._platform_two = Platform((self._width / 2 - 107 / 2,
                                       self._surface.get_height() - 270), (107, 30), self.article_list[1], False)
        self._platform_three = Platform((self._width - 107, self._surface.get_height() - 270), (107, 30),
                                        self.article_list[2], False)
        self._platform_group = pygame.sprite.Group(self._platform_one, self._platform_two, self._platform_three)
        # character attributes
        self._character = MainCharacter(self._ground.rect.midtop, list(self._platform_two.rect.midtop))
        # powerup & debuff attributes
        self.powerup = PowerUp((0, self._surface.get_width()), (0, self._character.rect.top),
                               "data/gfx/internet_asset_packs/Animated pixel coins/coin2_20x20.png")
        self.debuff = PowerUp((0, self._surface.get_width()), (0, self._character.rect.top),
                              "data/gfx/internet_asset_packs/Animated pixel coins/coin3_20x20.png")
        # for every 3 platforms in the platform group, blit a randomly generated word on the screen
        self.generate_draw_word(self._platform_group.sprites()[0].rect[0:2])
        self.max_platforms = 12
        # loading bar to serve as powerup timer
        self.loading_bar = LoadingBar(self._surface)
        self.loading_bar.rescale_lb(1.7)
        # fonts
        self.main_font = "data/fonts/Roboto_Condensed/RobotoCondensed-Regular.ttf"
        # formatting code
        self.format_panel_screen()
        # guess timer variables
        self.guess_timer_text = Text("0", (0, 0, 0), 25, (15, 50))
        self.guess_timer_last_time = 0
        self.guess_timer_var = 10000
        self.guess_timer_bool = True
        self.show_guess_timer = True
        # menu attributes
        # button objects
        self.resume_button = Button((185, 72), (self._surface.get_rect().centerx, 160),
                                    pygame.image.load("data/gfx/internet_asset_packs/"
                                                      "Menu Image Sprites/button_resume.png"), 1)
        self.settings_button = Button((199, 72), (self._surface.get_rect().centerx, 310),
                                      pygame.image.load("data/gfx/internet_asset_packs/"
                                                        "Menu Image Sprites/button_options.png"), 1)
        self.exit_button = Button((122, 72), (self._surface.get_rect().centerx, 460),
                                  pygame.image.load("data/gfx/internet_asset_packs/"
                                                    "Menu Image Sprites/button_quit.png"), 1)
        self.video_settings_button = Button((341, 72), (self._surface.get_rect().centerx, 150),
                                            pygame.image.load("data/gfx/internet_asset_packs/"
                                                              "Menu Image Sprites/button_video.png"), 1)
        self.audio_settings_button = Button((341, 72), (self._surface.get_rect().centerx, 300),
                                            pygame.image.load("data/gfx/internet_asset_packs/"
                                                              "Menu Image Sprites/button_audio.png"), 1)
        self.key_bindings_button = Button((302, 72), (self._surface.get_rect().centerx, 450),
                                          pygame.image.load("data/gfx/internet_asset_packs/"
                                                            "Menu Image Sprites/button_keys.png"), 1)
        self.back_button = Button((129, 72), (self._surface.get_rect().centerx, 600),
                                  pygame.image.load("data/gfx/internet_asset_packs/"
                                                    "Menu Image Sprites/button_back.png"), 1)
        self.confirm_button = Button((199, 72), (self._surface.get_rect().centerx, 600),
                                     pygame.image.load("data/gfx/internet_asset_packs/"
                                                       "Menu Image Sprites/button_confirm.png"), 1)

        # game variables
        self.coins = 0
        self.stage = 0
        self.background_scroll = 0
        self.coin_multipler = 1
        self.lowest_word_rating = 0
        self.pause_duration_guess_timer = 0
        self.running = True
        self.menu_running = False
        self.gameover = False
        self.moving_platforms = False
        self.increase_rating = False
        self.punish_articles = False
        self.reverse_inputs_var = False
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
        # move_result_tuple = (scroll, stage_changed)
        scroll, stage_changed = self._character.move(self._ground.rect.y, self._platform_group,
                                                     self._surface.get_rect()[2:], self.stage, self.reverse_inputs_var)
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
        # Animated pixel coins UI elements
        self._surface.blit(self._wooden_frame, (-30, -14))
        self.draw_score()
        # heart UI elements
        self._surface.blit(self._wooden_frame, (370, -14))
        self.draw_hearts()
        # check if gameover condition is met
        if self.gameover_check(stage_changed):
            self.gameover = True
        # guess timer UI elements & logic
        if self.show_guess_timer:
            self._surface.blit(self._wooden_frame, (170, -14))
            self.format_guess_timer(self.guess_timer_method(stage_changed)[1])
            self.guess_timer_text.rect.topleft = (235, -3)
            self.guess_timer_text.draw_on_surface(self._surface)
        # check if user has made correct decision
        if self._character.on_platform != "":
            if not self.check_answer():
                self.deduct_hearts()
            self._character.on_platform = ""
        # powerup logic + UI
        # make it so that there's a 1 in 500 chance a powerup spawns
        self.powerup.assess_draw_powerup()
        if self.powerup.draw_powerup and not self.debuff.power_up_active:
            self.powerup.draw_on_screen(self._surface, scroll, self._character)
        self.double_coins()
        # debuff logic + UI
        # 1 in a 500 chance debuff spawnspowerup.
        self.powerup.assess_draw_powerup()
        # reverse the player's left and right inputs if debuff is picked up
        self.debuff.assess_draw_powerup()
        if self.debuff.draw_powerup and not self.powerup.power_up_active:
            self.debuff.draw_on_screen(self._surface, scroll, self._character)
        self.reverse_inputs_method()
        # as user progresses, make the game harder by choosing harder words and making the game more dynamic
        self.raise_difficulty()
        # if timer_started runs out, delete powerup.
        self._frame.update()

    def double_coins(self):
        # if user collected the powerup and it's still in effect, double the amount of Animated pixel coins earned
        if self.powerup.power_up_active:
            self.coin_multipler = 2
            # blit loading bar
            self.loading_bar.resize_bar(self.powerup.last_time_effect, self.powerup.pause_duration_effect)
            self.loading_bar.draw_on_screen()
            if self.powerup.effect_timer():
                self.powerup.power_up_active = False
                self.coin_multipler = 1
                self.powerup.pause_duration_effect = 0
                self.loading_bar.bar_obj_list.clear()

    def reverse_inputs_method(self):
        if self.debuff.power_up_active:
            self.reverse_inputs_var = True
            self.loading_bar.resize_bar(self.debuff.last_time_effect, self.debuff.pause_duration_effect)
            self.loading_bar.draw_on_screen()
            if self.debuff.effect_timer():
                self.debuff.power_up_active = False
                self.reverse_inputs_var = False
                self.debuff.pause_duration_effect = 0
                self.loading_bar.bar_obj_list.clear()

    def format_guess_timer(self, guess_timer: int) -> None:
        if guess_timer >= 1000:
            self.guess_timer_text.change_text(str(guess_timer)[0] + "." + str(guess_timer)[1])
        elif guess_timer < 1000:
            self.guess_timer_text.change_text("0." + str(guess_timer)[0])
        elif guess_timer < 100:
            self.guess_timer_text.change_text("0.0")

    def draw_score(self):
        coin_sprite = load_sprite(pygame.image.load(
            "data/gfx/internet_asset_packs/Animated pixel coins/coin2_20x20.png"),
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
            self.increase_rating = False
        if self.coins % 1000 != 0:
            self.increase_rating = True

    def draw_hearts(self):
        first_x_coord = 390
        x_coord_increment = 40
        max_hearts = 0
        break_loops = False
        for i in range(2):
            for x in range(self._character.lives[i]):
                if i == 0:
                    self._surface.blit(self._whole_heart, (first_x_coord, -2))
                if i == 1:
                    self._surface.blit(self._half_heart, (first_x_coord-2, -2))
                if max_hearts < 2:
                    max_hearts += 1
                else:
                    max_hearts = 0
                    break_loops = True
                    break
                first_x_coord += x_coord_increment
            if break_loops:
                break
        first_x_coord = 470
        for i in range(self._character.lives[2]):
            self._surface.blit(self._empty_heart, (first_x_coord, -2))
            first_x_coord -= x_coord_increment

    def gameover_check(self, stage_changed):
        if (self._character.lives[1]+self._character.lives[0]) <= 0:
            return True
        if self._character.rect.top > self._surface.get_height():
            self.deduct_hearts()
            if self._character.last_saved_pos in [list(platform.rect.midtop)
                                                  for platform in self._platform_group.sprites()]:
                self._character.rect.midbottom = self._character.last_saved_pos
            else:
                self._character.last_saved_pos = list(self._platform_group.sprites()[1].rect.midtop)
                self._character.rect.midbottom = self._character.last_saved_pos
        if self.show_guess_timer:
            if not self.guess_timer_method(stage_changed)[0]:
                self.deduct_hearts()

    def deduct_hearts(self):
        if self._character.lives_pos == 0:
            self._character.lives[0] -= 1
            if self._character.lives[1]:
                self._character.lives_pos += 1
            else:
                self._character.lives_pos += 2
        elif self._character.lives_pos == 1:
            self._character.lives[1] -= 1
            self._character.lives_pos += 1
        if self._character.lives_pos == 2:
            self._character.lives[2] += 1
            self._character.lives_pos = 0

    def main_menu(self):
        pause_timer = 0
        menu_state = "main"
        user_input_ls = [["Heart Amount:", "", 0, False, pygame.rect.Rect(0, 0, 0, 0), (1, 7), 1],
                         ["Disable Guess Timer:", "", 0, False, pygame.rect.Rect(0, 0, 0, 0), (0, 2), 1],
                         ["Article evaluation:", "", 0, False, pygame.rect.Rect(0, 0, 0, 0), (0, 2), 1]]
        while self.menu_running:
            if pause_timer == 0:
                pause_timer = pygame.time.get_ticks()
            self._surface.fill((0, 128, 128))
            if menu_state == "main":
                if self.resume_button.draw_on_screen(self._surface):
                    self.menu_running = False
                    if self.guess_timer_last_time:
                        self.pause_duration_guess_timer += pygame.time.get_ticks() - pause_timer
                    if self.powerup.last_time_draw:
                        self.powerup.pause_duration_draw += pygame.time.get_ticks() - pause_timer
                    if self.powerup.last_time_effect:
                        self.powerup.pause_duration_effect += pygame.time.get_ticks() - pause_timer
                if self.exit_button.draw_on_screen(self._surface):
                    self.running = False
                    self.menu_running = False
                if self.settings_button.draw_on_screen(self._surface):
                    menu_state = "options"
            elif menu_state[:7] == "options":
                if self.video_settings_button.draw_on_screen(self._surface):
                    menu_state = "video_settings"
                if self.audio_settings_button.draw_on_screen(self._surface):
                    pass
                if self.key_bindings_button.draw_on_screen(self._surface):
                    pass
                if self.back_button.draw_on_screen(self._surface) and menu_state != "options_register":
                    menu_state = "main"
                if menu_state == "options_register":
                    menu_state = "options"
            elif menu_state == "video_settings":
                # draw objects to surface
                for counter, i in enumerate(user_input_ls):
                    # check how many chars are in input rect and adjust size
                    rect_color = pygame.Color("gray")
                    if len(i[1]) != 0:
                        i[2] = len(i[1]) * 7 + 10
                    else:
                        i[2] = 10
                    if i[3]:
                        rect_color = pygame.Color("white")
                    # create option static text
                    option_static_text = Text(i[0], (0, 0, 0), 30, (self.confirm_button.rect.center[0],
                                                                    (counter+1)*100), self.main_font)
                    # set the input rect
                    i[4] = pygame.rect.Rect(0, 0, i[2], 30)
                    i[4].midleft = (option_static_text.rect.midright[0]+5, (counter+1)*100)
                    # create input static text
                    input_static_text = Text(i[1], (0, 0, 0), 20, (i[4].midleft[0]+5, i[4].midleft[1]), self.main_font,
                                             True)
                    # draw text variables onto surface
                    option_static_text.draw_on_surface(self._surface)
                    input_static_text.draw_on_surface(self._surface)
                    pygame.draw.rect(self._surface, rect_color, i[4], 2)
                if self.confirm_button.draw_on_screen(self._surface):
                    menu_state = "options_register"
                    if user_input_ls[0][1]:
                        # change in-game life amount (takes effect after user dies)
                        self._character.next_lives = [0, 0, 0]
                        if int(user_input_ls[0][1]) <= 3:
                            self._character.next_lives[0] = int(user_input_ls[0][1])
                        else:
                            self._character.next_lives[0] = int(user_input_ls[0][1]) - 3
                            self._character.next_lives[1] = int(user_input_ls[0][1]) - self._character.next_lives[0]
                    # Remove guess timer if true
                    if user_input_ls[1][1] == "1":
                        self.show_guess_timer = False
                    elif user_input_ls[1][1] == "0":
                        self.show_guess_timer = True
                    # Wrong articles cause a loss of hearts if true
                    if user_input_ls[2][1] == "1":
                        self.punish_articles = True
                    elif user_input_ls[2][1] == "0":
                        self.punish_articles = False
                        if self._character.lives[0] == 1 and not self._character.lives[1] or not \
                                self._character.lives[0] and self._character.lives[1] == 1:
                            print("MA I FOUND A CHEATAH!")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.menu_running = False
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # check if input rect is active or not
                    for i in user_input_ls:
                        mouse_cursor = pygame.mouse.get_pos()
                        if i[4].collidepoint(mouse_cursor):
                            i[3] = True
                        else:
                            i[3] = False
                if event.type == pygame.KEYDOWN and menu_state == "video_settings":
                    for e in user_input_ls:
                        if e[3]:
                            if event.key == pygame.K_BACKSPACE:
                                if len(e[1]) != 0:
                                    e[1] = e[1][:len(e[1])-1]
                            elif event.unicode in [str(i) for i in range(*e[5])] and len(e[1]) < e[6]:
                                e[1] += event.unicode

            self._frame.update()

    def check_answer(self) -> bool:
        # check what stage the user is at to make sure the guess is being made for the right word
        if self.word_article_list[self.stage][1] == self._character.on_platform:
            self.coins += 50 * self.coin_multipler
        elif self.punish_articles and self.word_article_list[self.stage][1] != self._character.on_platform:
            return False
        return True

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
        self.guess_timer_bool = True
        self.lowest_word_rating = 0
        self._character.platform_stage = -1
        self._character.on_platform = ""
        self.moving_platforms = False
        # reset character, ground and platform positions
        self._character.lives = copy.deepcopy(self._character.next_lives)
        self._ground.rect.x = 0
        self._ground.rect.y = self._surface.get_size()[1]-100
        self._character.jumping = False
        self._character.rect.midbottom = self._ground.rect.midtop
        self._platform_group.empty()
        random.shuffle(self.article_list)
        self._platform_one = Platform((0, self._surface.get_height() - 270), (107, 30), self.article_list[0], False)
        self._platform_two = Platform((self._width / 2 - 107 / 2,
                                       self._surface.get_height() - 270), (107, 30), self.article_list[1], False)
        self._platform_three = Platform((self._width - 107, self._surface.get_height() - 270), (107, 30),
                                        self.article_list[2], False)
        self._platform_group.add(self._platform_one, self._platform_two, self._platform_three)
        self.word_article_dict = {}
        self.word_article_list = []
        self.generate_draw_word(self._platform_group.sprites()[0].rect[0:2])

    def guess_timer_method(self, stage_changed):
        if self.guess_timer_bool:
            self.guess_timer_last_time = pygame.time.get_ticks()
            self.guess_timer_bool = False
        current_time = pygame.time.get_ticks()
        time_change = current_time - self.guess_timer_last_time - self.pause_duration_guess_timer
        if time_change <= self.guess_timer_var:
            if stage_changed:
                self.guess_timer_bool = True
                self.pause_duration_guess_timer = 0
            return True, time_change
        else:
            self.guess_timer_bool = True
            self.pause_duration_guess_timer = 0
            return False, time_change

    # getter and setter decorators
    @property
    def surface(self):
        return self._surface

    @property
    def frame(self):
        return self._frame


def draw_game_over_text(main_frame, coins):
    game_over_text = Text("GAME OVER", (255, 255, 255), 50,
                          (main_frame.surface.get_rect().centerx, main_frame.surface.get_rect().centery - 50),
                          main_frame.main_font)
    score_text = Text("SCORE: " + str(coins), (255, 255, 255), 50,
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
                draw_game_over_text(game_window, game_window.coins)
                if update_frame:
                    game_window.frame.update()
                    update_frame = False
                key = pygame.key.get_pressed()
                if key[pygame.K_SPACE]:
                    update_frame = True
                    game_window.reset_game_variables()
        else:
            game_window.main_menu()
