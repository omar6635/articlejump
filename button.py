import pygame
from load_sprite import load_sprite


class Button(pygame.sprite.Sprite):
    def __init__(self, dimensions: tuple, coordinates: tuple, image, scale):
        super(Button, self).__init__()
        self.image = load_sprite(image, 30, 93, *dimensions, scale, (0, 0, 0))
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
    resume_img = pygame.image.load("data/gfx/exit_button.png").convert_alpha()
    button = Button((240, 117), display.get_rect().center, resume_img, 0.6)
    run = True
    while run:
        display.fill((55, 55, 55))
        # draw rect
        pygame.draw.rect(display, (255, 255, 255), button.rect, 1)
        button.draw_on_screen(display)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
    pygame.quit()
