import pygame

# radiu for the circle
RADIUS = 4 * 50

# define the size of the window
HEIGHT = 850
LENGTH = 1350

# class for drawing the dark area onto the map
class Dark:
    def __init__(self, x, y):
        self.center_x = x
        self.center_y = y
        self.radius = RADIUS
        # create a circular mask
        self.mask = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.mask, (0, 0, 0, 200), (self.radius, self.radius), self.radius)

    def make_dark(self, surface):
        # create a transparent mask
        mask = pygame.Surface((LENGTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(mask, (0, 0, 0, 200), (self.center_x, self.center_y), self.radius)

        # blit the transparent mask to reveal the background within the circle
        surface.blit(mask, (0, 0))

    # update the circle center
    def change_pos(self, x, y):
        # adding half of the player size
        self.center_x = x + 8 
        self.center_y = y + 8