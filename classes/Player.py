from .Point import Point
from .Animate import Animate
import pygame


VELOCITY = 8

HEIGHT = 750
LENGTH = 1250

SQUARE = 50

# class for handling players
class Player(Point, Animate):

    # init the atributes of player obj
    def __init__(self, x, y, state, image, screen):
        self.position = Point(x, y)
        self.image = Animate(image, state, screen)
        self.velocity = VELOCITY
        self.position_in_matrix_i = 2
        self.position_in_matrix_j = 2
        self.save_x = x
        self.save_y = y
        self.bullets = 20
        self.health = 1
        self.bullet_array = [None] * 20 # maximum 20 bullets
        self.active_bullets = 0
        # the initial state of the player for animation
        self.state = state

    def reset_player(self):
        self.position_in_matrix_i = 2
        self.position_in_matrix_j = 2
        self.bullets = 20
        self.health = 1
        self.position.x = self.save_x
        self.position.y = self.save_y
        self.bullet_array = [None] * 20 # maximum 10 bullets
        self.active_bullets = 0

    # method that changes the state of the player
    def find_direction(self, x, y):

        # find the direction
        if (self.position.y > y and self.position.x == x):
            return "UP"
        if (self.position.y < y and self.position.x == x):
            return "DOWN"
        if (self.position.x > x and self.position.y == y):
            return "LEFT"
        if (self.position.x < x and self.position.y == y):
            return "RIGHT"

        # change the position
    
    def move(self, new_x, new_y, map):
        rect = self.image.square_surface.get_rect(topleft=(new_x, new_y))
        
        for i in range(0, 25, 1): # TODO check just in the middle for optimisation
            for j in range(0, 15, 1):

                block = map.display_matrix[i][j].rect
                if map.display_matrix[i][j].block_type == 1 and self.collide(block, rect) == True:
                    return False
                elif map.display_matrix[i][j].block_type == 4 and self.collide(block, rect) == True:
                    # TODO implement exit logic
                    # reset coords
                    self.position.x = 100
                    self.position.y = 100
                    self.position_in_matrix_i = 2
                    self.position_in_matrix_j = 2
                    return True
                elif map.display_matrix[i][j].block_type == 0 and self.collide(block, rect) == True:
                    self.position_in_matrix_i = i
                    self.position_in_matrix_j = j

        # find the direction of the player
        new_state = self.find_direction(new_x, new_y)
        
        # get the handle of the player box
        self.image.animate(new_state)
        
        self.state = new_state
        # modify the coords
        self.position.change_x(new_x)
        self.position.change_y(new_y)
        return False
        
    def collide(self, block_rect, player_rect):
        if player_rect.colliderect(block_rect):
            # calculate the overlap on each side
            overlap_left = block_rect.right - player_rect.left
            overlap_right = player_rect.right - block_rect.left
            overlap_top = block_rect.bottom - player_rect.top
            overlap_bottom = player_rect.bottom - block_rect.top

            # check which side has the minimum overlap
            min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

            if min_overlap == overlap_left:
                return True
            elif min_overlap == overlap_right:
                return True
            elif min_overlap == overlap_bottom:
                return True
            elif min_overlap == overlap_top:
                return True

        return False

    def add_bullet(self, bullet):
        self.bullet_array[self.active_bullets] = bullet
        self.active_bullets += 1
        # decrement the number of bullets
        self.bullets -= 1

    def remove_bullet(self, bullet):
        for i in range(0, self.active_bullets, 1):
            if self.bullet_array[i] == bullet:
                self.active_bullets -= 1
                
    def display_health(self, screen):
        image = pygame.transform.scale(pygame.image.load("docs/blocks/" + "health.png").convert_alpha(), (SQUARE, SQUARE))
        for i in range(1, 4, 1):
            if i <= self.health:
                health_icon_x = LENGTH - i * (SQUARE)
                health_icon_y = 0
                screen.blit(image, (health_icon_x, health_icon_y))