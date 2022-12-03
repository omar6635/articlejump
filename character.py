import pygame
from load_sprite import load_sprite


class MainCharacter(pygame.sprite.Sprite):
    def __init__(self, coordinates):
        super(MainCharacter, self).__init__()
        self.sprite = pygame.image.load("data/gfx/internet_asset_packs/Medieval King Pack 2/Sprites/Idle.png")\
            .convert_alpha()
        # 63, 223, 383 ...
        self.image = load_sprite(self.sprite, 64, 50, 34, 56, 1, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.midbottom = coordinates
        self._velocity = 3
        self._jump_velocity = 0
        self._gravity = 1
        self.last_time = pygame.time.get_ticks()
        self.animation_cooldown = 100
        self.frame = 0
        self.animation_mode = 0
        self.jumping = False
        self.flip = False
        self.scroll_threshold = None
        self.lives = 3
        self.last_saved_pos = 0

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

    def check_jump(self, dy: int):
        if dy < 0:
            self.animation_mode = 2
        elif dy > 0:
            self.animation_mode = 3

    def move(self, ground_top,  platform_group, screen_dimensions):
        # reset variables
        scroll = 0
        dx = 0
        dy = 0
        collision_detected = False
        s_width = screen_dimensions[0]
        self.scroll_threshold = screen_dimensions[1]/2

        # process keypresses
        self.handle_input(s_width)

        # gravity
        if self.jumping:
            self._jump_velocity += self._gravity
            dy += self._jump_velocity

        # check collision with platform
        for platform in platform_group:
            # collision in the y direction
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                # check if above the platform
                if self.rect.bottom < platform.rect.centery:
                    if self.jump_velocity > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.jumping = False
                        self.last_saved_pos = platform.rect.midtop
                        collision_detected = True

        # check if user is hovering over nothing and if so, drop him
        if self.rect.y != 596 and dy == 0 and not self.jumping and not collision_detected:
            self.jumping = True
            self.jump_velocity = 0

        # check collision with ground
        if self.rect.bottom + dy > ground_top:
            self.jumping = False

        # check if the player has bounced to the top of the screen
        if self.rect.top <= self.scroll_threshold:
            # if player is jumping
            if self.jump_velocity < 0:
                scroll = -dy+1

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy + scroll

        self.check_jump(dy)
        return scroll

    def handle_input(self, screen_width):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if self.allow_traversal(screen_width) != "r border":
                self.rect.x += self.velocity
                if not self.jumping:
                    self.animation_mode = 1
                self.flip = False
        elif keys[pygame.K_LEFT]:
            if self.allow_traversal(screen_width) != "l border":
                self.rect.x -= self.velocity
                if not self.jumping:
                    self.animation_mode = 1
                self.flip = True
        else:
            self.animation_mode = 0
        if keys[pygame.K_UP] and not self.jumping:
            self.jumping = True
            self._jump_velocity = -20

    def allow_traversal(self, surface_width) -> str:
        """
        allows for the user to go beyond the borders and pop out on the other side

        :return: String
        """
        if self.rect.x < -1 * self.rect.size[0]/2:
            self.rect.x = surface_width-self.rect.size[0]/2
            return "l border"
        if self.rect.bottomright[0] > surface_width+self.rect.size[0]/2:
            self.rect.x = -1 * self.rect.size[0]/2
            return "r border"

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
    my_char = MainCharacter((500, 500))
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
