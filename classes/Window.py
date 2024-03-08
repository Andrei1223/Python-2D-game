import pygame
import sys
from pygame.locals import *
from classes.Player import Player
from classes.Dark import Dark
from classes.Map import Map

class Window:
    def __init__(self):
        pygame.init()

        # Set up the window
        self.HEIGHT = 800
        self.LENGTH = 1300
        self.screen = pygame.display.set_mode((self.LENGTH, self.HEIGHT))
        pygame.display.set_caption("Game Window")

        # Set up the clock
        self.clock = pygame.time.Clock()

        # Initialize game state
        self.running = True
        self.state_of_game = False  # Initially, not in the game
        self.in_game_menu = False

        # Initialize player and map
        self.hero = None
        self.darkness = None
        self.map = None

        # Initialize buttons
        self.return_button_rect = pygame.Rect(10, 10, 200, 50)
        self.exit_button_rect = pygame.Rect(550, 350, 200, 50)
        self.map_displayed = False

    def start_menu(self):
        # Implement your menu logic here
        pass

    def start_game(self):
        # Initialize the game components
        self.hero = Player(100, 100, "UP", "docs/hero/hero_", self.screen)
        self.darkness = Dark(self.hero.position.x, self.hero.position.y)
        self.map = Map(200, 100)
        
        # Show the map
        self.map.show_map(self.screen, 0, 0, min(self.LENGTH // 2, self.HEIGHT // 2))

        self.screen.blit(self.hero.image.square_surface,
                                            (self.hero.position.x, self.hero.position.y))

        # Set game state to True to indicate the game is running
        self.state_of_game = True
        self.map_displayed = True

        # Set in-game menu state to False
        self.in_game_menu = False

    def in_game_menu_screen(self):
        # Display in-game menu screen
        self.screen.fill((128, 128, 128))

        if self.map_displayed:
            pygame.draw.rect(self.screen, (0, 0, 255), self.return_button_rect)
            button_font = pygame.font.Font(None, 36)
            return_text_surface = button_font.render("Return", True, (255, 255, 255))
            return_text_rect = return_text_surface.get_rect(topleft=(20, 20))
            self.screen.blit(return_text_surface, return_text_rect)

        pygame.draw.rect(self.screen, (255, 0, 0), self.exit_button_rect)
        exit_text_surface = button_font.render("Exit", True, (255, 255, 255))
        exit_text_rect = exit_text_surface.get_rect(center=self.exit_button_rect.center)
        self.screen.blit(exit_text_surface, exit_text_rect)

        pygame.display.flip()

    def check_key(self):
        keys = pygame.key.get_pressed()
        x = self.hero.position.x
        y = self.hero.position.y

        if keys[K_w]:
            y -= self.hero.velocity
            self.hero.move(x, y, self.map.matrix)
        if keys[K_s]:
            y += self.hero.velocity
            self.hero.move(x, y, self.map.matrix)
        if keys[K_a]:
            x -= self.hero.velocity
            self.hero.move(x, y, self.map.matrix)
        if keys[K_d]:
            x += self.hero.velocity
            self.hero.move(x, y, self.map.matrix)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.in_game_menu:
                        if self.return_button_rect.collidepoint(event.pos):
                            self.in_game_menu = False
                        elif self.exit_button_rect.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()
                    elif self.state_of_game:
                        if self.map_is_clicked(event.pos):
                            self.in_game_menu = True

            self.screen.fill((128, 128, 128))

            if not self.state_of_game:
                self.start_menu()
            else:
                self.darkness.change_pos(self.hero.position.x, self.hero.position.y)
                self.darkness.make_dark(self.screen)
                self.check_key()
                self.screen.blit(self.hero.image.square_surface,
                                            (self.hero.position.x, self.hero.position.y))

                if self.in_game_menu:
                    self.in_game_menu_screen()

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

    def map_is_clicked(self, pos):
        x_map_start, y_map_start = 0, 0
        map_width, map_height = 50, 50

        return (
            x_map_start <= pos[0] <= x_map_start + 400 and
            y_map_start <= pos[1] <= y_map_start + 400
        )

# Run the game
if __name__ == "__main__":
    game_window = Window()
    game_window.run()
