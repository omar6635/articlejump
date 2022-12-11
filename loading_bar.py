import pygame


class LoadingBar(pygame.sprite.Sprite):
    def __init__(self, surface: pygame.Surface):
        super(LoadingBar, self).__init__()
        self.surface = surface
        self.bg_image = pygame.image.load("data/gfx/internet_asset_packs/"
                                          "GUI Interface Kit Free/PNG/GUI-Kit-Pack-Free_35.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (self.bg_image.get_size()[0]+10,
                                                               self.bg_image.get_size()[1]))
        self.bg_image_rect = self.bg_image.get_rect()
        self.set_bg_coordinates()
        self.bar_image = pygame.image.load("data/gfx/internet_asset_packs/"
                                           "GUI Interface Kit Free/PNG/GUI-Kit-Pack-Free_04.png")
        self.bar_image_rect = self.bar_image.get_rect()
        self.bar_image_rect.midleft = self.bg_image_rect.midleft
        self.bar_obj_list = []
        self.progress = 0
        self.timer = 2000

    def draw_on_screen(self):
        for obj_rect in self.bar_obj_list:
            self.surface.blit(self.bar_image, obj_rect)
        self.surface.blit(self.bg_image, self.bg_image_rect)

    def set_bg_coordinates(self):
        self.bg_image_rect.center = self.surface.get_rect().midbottom
        self.bg_image_rect.centery -= 50

    def resize_bar(self, last_time, pause_duration):
        current_time = pygame.time.get_ticks()
        current_progress = current_time - last_time - pause_duration
        bars_needed = self.bg_image.get_size()[0] // self.bar_image.get_size()[0]
        if current_progress <= self.timer:
            self.progress = current_progress / self.timer * (self.bar_image.get_size()[0] * bars_needed)
            x_offset = self.progress // self.bar_image.get_size()[0] * self.bar_image.get_size()[0]
            bar_object_rect = self.bg_image_rect.x + x_offset, self.bg_image_rect.y+3
            self.bar_obj_list.append(bar_object_rect)

    def rescale_lb(self, division_factor):
        self.bg_image = pygame.transform.scale(self.bg_image, (self.bg_image.get_size()[0] / division_factor,
                                               self.bg_image.get_size()[1] / division_factor))
        self.bg_image_rect = self.bg_image.get_rect()
        self.set_bg_coordinates()
        self.bar_image = pygame.transform.scale(self.bar_image, (self.bar_image.get_size()[0] / division_factor,
                                                self.bar_image.get_size()[1] / division_factor))
        self.bar_image_rect = self.bar_image.get_rect()


if __name__ == "__main__":
    pygame.init()
    display = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()
    loading_bar = LoadingBar(display)
    running = True
    outer_last_time = pygame.time.get_ticks()
    loading_bar.rescale_lb(1.7)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
        display.fill((0, 0, 0))
        loading_bar.resize_bar(outer_last_time)
        loading_bar.draw_on_screen()
        pygame.display.update()
        clock.tick(60)
