import pygame
from loadSprite import load_sprite


class MainCharacter(pygame.sprite.Sprite):
    def __init__(self, coordinates):
        super(MainCharacter, self).__init__()
        self.sprite = pygame.image.load("data/gfx/internet_asset_packs/Medieval King Pack 2/Sprites/Idle.png")\
            .convert_alpha()
        self.image = load_sprite(self.sprite, 0, 160, 111, 1, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.reset_position(coordinates)
        self._velocity = 3
        self._jump_velocity = 20
        self._accelr = 1
        self.last_time = pygame.time.get_ticks()
        self.animation_cooldown = 100
        self.frame = 0
        self.animation_mode = 0
        self.flip = False

    def reset_position(self, coordinates):
        self.rect.x = coordinates[0]/2
        self.rect.y = coordinates[1] - self.rect.size[1]*1.39

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
            for x in range(steps):
                temp_list.append(load_sprite(self.sprite, x, 160, 111, 1, (0, 0, 0)))
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
    def accelr(self):
        return self._accelr

    @accelr.setter
    def accelr(self, val):
        self._accelr = val


if __name__ == "__main__":
    pygame.init()
    display = pygame.display.set_mode((500, 500))
    my_char = MainCharacter((250, 0))
    run = True
    while run:
        display.fill((55, 55, 55))
        loop_animation = my_char.create_animation_list()
        my_char.animation(loop_animation, display)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
    pygame.quit()
