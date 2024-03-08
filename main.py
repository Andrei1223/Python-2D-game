# Example file showing a basic pygame "game loop"
from classes.Player import Player
from classes.Dark import Dark
from classes.Map import Map
from classes.Bullet import Bullet
from classes.Enemy import Enemy
from pygame.locals import *
import pygame
import time
import sys
import random

# define the size of the window
HEIGHT = 750
LENGTH = 1250

# pygame setup
pygame.init()
screen = pygame.display.set_mode((LENGTH, HEIGHT))
clock = pygame.time.Clock()
running = True
can_continue = False
in_menu = True
start_game = False

# define the state of the game
state_of_game = False
level = -1

# define the player and enemies
hero = Player(100, 100, "UP", "docs/hero/hero_", screen)
enemies = [None] * 30
enemies_cnt = 0
darkness = Dark(hero.position.x, hero.position.y)

# define the map with a size divisible by 25
map = Map(75, 75)

# read the difficulty
dificulty = "EASY"
while (dificulty := input("Select difficulty (EASY/MEDIUM/HARD): ")) and (dificulty not in ["EASY", "MEDIUM", "HARD"]):
    print("Wrong format!")

# function to draw buttons on the screen
def draw_button(screen, rect, text, font, highlight=False, disabled=False):
    if disabled:
        color = (169, 169, 169)
    else:
        color = (255, 255, 255)

    if highlight:
        color = (200, 200, 200)

    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, (0, 0, 0), rect, 2)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

# function to check for input
def check_key(dist):
    keys = pygame.key.get_pressed()
    dist[0] = hero.position.x
    dist[1] = hero.position.y
    
    result = False
    if keys[K_w]:
        # "W" key is pressed, move the player up
        dist[1] -= hero.velocity
        dist
        result = hero.move(dist[0], dist[1], map)
        time.sleep(0.05)
    elif keys[K_s]:
        # "S" key is pressed, move the player down
        dist[1] += hero.velocity
        result =  hero.move(dist[0], dist[1], map)
        time.sleep(0.05)
    elif keys[K_a]:
        # "A" key is pressed, move the player left
        dist[0] -= hero.velocity
        result = hero.move(dist[0], dist[1], map)
        time.sleep(0.05)
    elif keys[K_d]:
        # "D" key is pressed, move the player right
        dist[0] += hero.velocity
        #if map.
        result = hero.move(dist[0], dist[1], map)
        time.sleep(0.05)
    # create bullet
    if keys[K_SPACE]:
        time.sleep(0.08)
        # if the player has bullets
        if hero.bullets > 0:
            bullet = Bullet(hero.position.x, hero.position.y, hero.image.state, 8)
            hero.add_bullet(bullet)
        return result    
    return result

def display_bullets():
    # hero s bullets
    for i in range(0, hero.active_bullets, 1):
        hero.bullet_array[i].draw(screen)
        target = [pygame.Rect] * enemies_cnt

        for j in range(0, enemies_cnt, 1):
            target[j] = enemies[j].rect

        result = hero.bullet_array[i].move(map, target)
          
        # the bullet has hit a wall
        if result == -1:
            hero.remove_bullet(hero.bullet_array[i])
        elif result != -2:
            # remove the health from the result-th enemy
            enemies[result].health -= 1
            #target[result].health -= 1
            hero.remove_bullet(hero.bullet_array[i])
            break
    
    # traverse the enemies
    rect = hero.image.square_surface.get_rect(topleft=(hero.position.x, hero.position.y))
    target = [pygame.Rect] * 1
    target[0] = rect
    for aux in range(0, enemies_cnt, 1):
        for i in range(0, enemies[aux].active_bullets, 1):
            enemies[aux].bullet_array[i].draw(screen)
            result = enemies[aux].bullet_array[i].move(map, target)

            # the bullet has hit a wall
            if result == -1:
                enemies[aux].remove_bullet(enemies[aux].bullet_array[i])
            elif result == 0: # the bullet has hit the player
                hero.health -= 1 # remove health
                enemies[aux].remove_bullet(enemies[aux].bullet_array[i])
                time.sleep(0.05)

# from a certain box from the level return a random empty cell
def random_coords_from_box(box_index, difficulty):
    i_index = (box_index % 3) * 25
    j_index = (box_index // 3) * 15
    global enemies_cnt
    
    is_free = False

    while is_free == False:
        # generate random coords from the 2nd chunk
        x = random.randint(i_index + 4, i_index + 24)
        y = random.randint(j_index + 4, j_index + 14)
        is_free = False
        
        for i in range(0, enemies_cnt, 1):
            if enemies[i].x == x and enemies[i].y == y:
                is_free = False
                break
        if map.matrix[x][y].block_type == 0:
            is_free = True
    
    if is_free:
        # add a new enemy
        enemies[enemies_cnt] = Enemy(x % 25 * 50, y % 15 * 50, difficulty)
        enemies_cnt += 1
    else:
        print("problema")

# funtion that adds enemies for each level based on the difficulty
def add_enemies(level):
    global enemies_cnt
    enemies_cnt = 0
    # for EASY add 2 easy enemies and 1 medium
    if dificulty == "EASY":
        random_coords_from_box(level, "EASY")
        random_coords_from_box(level, "EASY")
        random_coords_from_box(level, "EASY")
    if dificulty == "MEDIUM":
        random_coords_from_box(level, "HARD")
        random_coords_from_box(level, "MEDIUM")
        random_coords_from_box(level, "EASY")
    if dificulty == "HARD":
        random_coords_from_box(level, "HARD")
        random_coords_from_box(level, "HARD")
        random_coords_from_box(level, "MEDIUM")
    
# function that displayes all the enemies from the current level
def show_enemies():
    rect = hero.image.square_surface.get_rect(topleft=(hero.position.x, hero.position.y))
    for i in range(0, enemies_cnt, 1):
        enemies[i].draw(screen)
        enemies[i].shot(rect)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif in_menu and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            # check if a button is clicked in the menu
            if continue_rect.collidepoint(mouse_pos) and can_continue:
                in_menu = False
                state_of_game = True
                start_game = False
            elif start_rect.collidepoint(mouse_pos):
                level = -1 # reset the level
                hero.reset_player() # reset the level
                map.level_index = -1 # reset the level
                in_menu = False
                state_of_game = True
                can_continue = True
                start_game = True
            elif exit_rect.collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()
    screen.fill((128, 128, 128)) 
    if in_menu:
        
        font = pygame.font.Font(None, 36)

        # continue Button
        continue_rect = pygame.Rect(500, 150, 300, 100)
        continue_highlight = continue_rect.collidepoint(pygame.mouse.get_pos())
        draw_button(screen, continue_rect, "Continue Game", font, continue_highlight, not can_continue)

        # start Button
        start_rect = pygame.Rect(500, 300, 300, 100)
        start_highlight = start_rect.collidepoint(pygame.mouse.get_pos())
        draw_button(screen, start_rect, "Start Game", font, start_highlight)

        # exit Button
        exit_rect = pygame.Rect(500, 450, 300, 100)
        exit_highlight = exit_rect.collidepoint(pygame.mouse.get_pos())
        draw_button(screen, exit_rect, "Exit", font, exit_highlight)
        
    else:
        screen.fill("purple") # TODO modify texture
        
        init_index = [hero.position_in_matrix_i, hero.position_in_matrix_j]
        dist = [0, 0]
        keys = pygame.key.get_pressed()
        if keys[K_q] and state_of_game:
            can_continue = True
            state_of_game = False
            in_menu = True

        # result is set on True if the player exits
        result = check_key(dist) # check for key input
        if start_game:
            result = True
            start_game = False

        map.show_map(screen, result)
        show_enemies()

        # if the player has advanced to another level
        if map.level_index != level:
            # reset bullets
            hero.reset_player()
            enemies_cnt = 0
            # add enemies
            add_enemies(map.level_index)
            # update the level
            level = map.level_index

        darkness.change_pos(hero.position.x, hero.position.y)
        darkness.make_dark(screen)
        hero.image.screen.blit(hero.image.square_surface, (hero.position.x, hero.position.y))
        display_bullets()
        hero.display_health(screen)
        
        if hero.health <= 0:
            # go to the menu
            can_continue = False
            state_of_game = False
            in_menu = True

        # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(30)  # limits FPS to 30

pygame.quit()