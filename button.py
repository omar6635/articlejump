import pygame
from load_sprite import load_sprite


class Button(pygame.sprite.Sprite):
    def __init__(self, dimensions: tuple, coordinates: tuple, image, scale):
        super(Button, self).__init__()
        self.image = load_sprite(image, 0, 2, *dimensions, scale, (0, 128, 128))
        self.rect = self.image.get_rect()
        self.rect.center = coordinates
        self.clicked = False

    def draw_on_screen(self, surface):
        pressed = False
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                pressed = True

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        surface.blit(self.image, self.rect)
        return pressed


if __name__ == "__main__":
    pygame.init()
    display = pygame.display.set_mode((500, 500))
    resume_img = pygame.image.load("data/gfx/internet_asset_packs/"
                                   "Menu Image Sprites/button_resume.png")
    button = Button((185, 72), display.get_rect().center, resume_img, 1)
    run = True
    while run:
        display.fill((0, 128, 128))
        # draw rect
        button.draw_on_screen(display)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
    pygame.quit()
