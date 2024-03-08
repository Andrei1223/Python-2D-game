import pygame
import time
from .Bullet import Bullet
import math

SQUARE = 50

class Enemy:
    def __init__(self, x, y, difficulty):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, SQUARE, SQUARE)
        self.bullet_array = [None] * 1000
        self.active_bullets = 0
        self.radius = 200 # TODO change the radius
        self.time = time.time()
        # these are set based on the dificulty
        self.image_path = ""
        self.delay = 10 # delay in seconds after each bullet
        self.bullets = 1000
        self.bullts_per_shot = 0
        self.health = 3
        self.bullet_velocity = 5
        self.directions = [str] * 4 # only in 4 dimensions for the hardest
        
        self.set_stats(difficulty)
        
        self.image = pygame.transform.scale(pygame.image.load(self.image_path).convert_alpha(), (SQUARE, SQUARE))
    
    # compute id the player is in the tower s radius
    def in_radius(self, rect):
        closest_point = (max(rect.left, min(self.x, rect.right)),
                    max(rect.top, min(self.y, rect.bottom)))
    
        distance = math.sqrt((self.x - closest_point[0])**2 + (self.y - closest_point[1])**2)

        return distance <= self.radius
        
    # pass the player rectangle for radius detection
    def shot(self, rect):
        # if the enemy has health
        if self.health <= 0:
            return
        # check if the time has passed
        if (time.time() - self.time) < self.delay:
            return
        
        # check if the player is in the radius
        if self.in_radius(rect) == False:
            return
        
        for i in range(0, self.bullts_per_shot, 1):
            for direction in self.directions:
                # create a new bullet
                self.add_bullet(Bullet(self.x, self.y, direction, self.bullet_velocity))
        
        # update the time
        self.time = time.time()

    def draw(self, screen):
        if self.health > 0:
            # draw the enemy using the image
            screen.blit(self.image, self.rect.topleft)
    
    def add_bullet(self, bullet):
        self.bullet_array[self.active_bullets] = bullet
        self.active_bullets += 1
        # decrement the number of bullets
        self.bullets -= 1

    def remove_bullet(self, bullet):
        for i in range(0, self.active_bullets, 1):
            if self.bullet_array[i] == bullet:
                self.active_bullets -= 1
        
    def set_stats(self, dificulty):
        
        if dificulty == "EASY":
            self.health = 1
            self.bullets = 15
            self.delay = 10
            self.bullts_per_shot = 1
            self.bullet_velocity = 10
            self.directions[0] = "UP"
            self.image_path = "docs/blocks/tower.png"
        elif dificulty == "MEDIUM":
            self.health = 2
            self.bullets = 30
            self.delay = 7
            self.bullts_per_shot = 1
            self.bullet_velocity = 8
            self.image_path = "docs/blocks/witch.png"
            self.directions[0] = "UP"
            self.directions[1] = "DOWN"
        elif dificulty == "HARD":
            self.health = 3
            self.bullets = 40
            self.delay = 5
            self.bullts_per_shot = 2
            self.bullet_velocity = 6
            self.image_path = "docs/blocks/wizz.png"
            self.directions[0] = "UP"
            self.directions[1] = "DOWN"
            self.directions[2] = "LEFT"
            self.directions[3] = "RIGHT"
            
