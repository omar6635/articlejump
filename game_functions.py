import pygame
from text import Text


def load_sprite(sprite: pygame.Surface, x, y, width, height, scale, color):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sprite, (0, 0), (x, y, width, height))
    # resize image
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(color)
    return image


def read_instructions(file_path: str) -> list:
    with open(file_path) as file:
        return [line.split() for line in file.readlines()]


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
    pygame.init()
    display = pygame.display.set_mode((500, 500))
    wooden_frame = load_sprite(pygame.image.load("data/gfx/internet_asset_packs/dungeon pack/wooden_frame.png"),
                               0, 0, 530, 174, 0.3, (0, 0, 0))
    whole_heart = load_sprite(pygame.image.load("data/gfx/internet_asset_packs/dungeonui.v1.png"),
                              20, 133, 14, 15, 2, (0, 0, 0))
    half_heart = load_sprite(pygame.image.load("data/gfx/internet_asset_packs/dungeonui.v1.png"),
                             35, 133, 14, 15, 2, (0, 0, 0))
    empty_heart = load_sprite(pygame.image.load("data/gfx/internet_asset_packs/dungeonui.v1.png"),
                              50, 133, 14, 15, 2, (0, 0, 0))
    run = True
    while run:
        display.fill((255, 255, 255))
        display.blit(wooden_frame, (200, 250))
        display.blit(whole_heart, (210, 267))
        display.blit(half_heart, (240, 267))
        display.blit(empty_heart, (270, 267))
        display.blit(empty_heart, (300, 267))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
    pygame.quit()
