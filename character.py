import pygame
from loadSprite import load_sprite


class MainCharacter(pygame.sprite.Sprite):
    def __init__(self, coordinates, ground_y):
        super(MainCharacter, self).__init__()
        self.sprite = pygame.image.load("data/gfx/internet_asset_packs/Medieval King Pack 2/Sprites/Idle.png")\
            .convert_alpha()
        # 63, 223, 383 ...
        self.image = load_sprite(self.sprite, 64, 50, 34, 56, 1, (0, 0, 0))
        self.rect = pygame.Rect(0, 0, 34, 56)
        self.reset_position(coordinates, ground_y)
        self._velocity = 3
        self._jump_velocity = 20
        self._gravity = 1
        self.last_time = pygame.time.get_ticks()
        self.animation_cooldown = 100
        self.frame = 0
        self.animation_mode = 0
        self.jumping = False
        self.flip = False
        self.on_platform = False

    def reset_position(self, coordinates, ground_y):
        self.rect.centerx = coordinates[0]/2
        self.rect.bottom = ground_y+2

    def create_animation_list(self):
        # create two dimensional list of sprite packs for idle, jumping, dead etc.
        sprite_list = ["data/gfx/internet_asset_packs/Medieval King Pack 2/Sprites/Idle.png",
                       "data/gfx/internet_asset_packs/Medieval King Pack 2/Sprites/Run.png",
                       "data/gfx/internet_asset_packs/Medieval King Pack 2/Sprites/Jump.png",
                       "data/gfx/internet_asset_packs/Medieval King Pack 2/Sprites/Fall.png"]
        animation_list = []
        for file in sprite_list:
            self.sprite = pygame.image.load(file).convert_alpha()
            steps = int(self.sprite.get_width() / 160)
            temp_list = []
            multiplier = 160
            for x in range(steps):
                temp_list.append(load_sprite(self.sprite, 63+multiplier*x, 50, 34, 56, 1, (0, 0, 0)))
            animation_list.append(temp_list)
        return animation_list

    def animation(self, animation_list, surface):
        current_time = pygame.time.get_ticks()
        if self.frame >= len(animation_list[self.animation_mode]):
            self.frame = 0
        if current_time - self.last_time >= self.animation_cooldown:
            self.frame += 1
            self.last_time = current_time
            if self.frame == len(animation_list[self.animation_mode]):
                self.frame = 0
        if not self.flip:
            surface.blit(animation_list[self.animation_mode][self.frame], self.rect)
        else:
            image_to_blit = pygame.transform.flip(animation_list[self.animation_mode][self.frame], True, False)\
                .convert_alpha()
            image_to_blit.set_colorkey((0, 0, 0))
            surface.blit(image_to_blit, self.rect)

    def check_jump(self, jump_velocity):
        if jump_velocity > 0:
            self.animation_mode = 2
        else:
            self.animation_mode = 3

    def jump(self, ground_y, platform_group):
        self.rect.y -= self._jump_velocity
        self._jump_velocity -= self.gravity

        if self.rect.bottom - self._jump_velocity > ground_y:
            self.jumping = False
            self._jump_velocity = 20
        if self.check_platform_collision(platform_group):
            self.jumping = False
            self.on_platform = True
            self._jump_velocity = 20

    def check_platform_collision(self, platform_group):
        # use collideobjects() for the rect class to test if character collides with platforms
        if self._jump_velocity < 0:
            if (self.rect.bottom - self._jump_velocity+8) > platform_group.sprites()[0].rect.y and \
                    MainCharacter.check_character_platform_col(platform_group, self.rect.centerx,
               self.rect.bottom - self._jump_velocity) or \
                    (self.rect.bottom - self._jump_velocity+8) > platform_group.sprites()[3].rect.y and \
                    MainCharacter.check_character_platform_col(platform_group, self.rect.centerx,
                                                               self.rect.bottom - self._jump_velocity):
                return True
            else:
                return False

    @staticmethod
    def check_character_platform_col(platform_group, x, y):
        for platform in platform_group:
            if platform.rect.collidepoint(x, y):
                return True
        return False

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, val):
        self._velocity = val

    @property
    def jump_velocity(self):
        return self._jump_velocity

    @jump_velocity.setter
    def jump_velocity(self, val):
        self._jump_velocity = val

    @property
    def gravity(self):
        return self._gravity

    @gravity.setter
    def gravity(self, val):
        self._gravity = val


if __name__ == "__main__":
    pygame.init()
    display = pygame.display.set_mode((500, 500))
    my_char = MainCharacter((500, 500), 400)
    run = True
    while run:
        display.fill((55, 55, 55))
        pygame.draw.rect(display, (0, 0, 0), my_char.rect, 2)
        loop_animation = my_char.create_animation_list()
        my_char.animation(loop_animation, display)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
    pygame.quit()
