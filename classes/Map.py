import pygame
import random
import time
from .Block import Block
from queue import Queue

path_to_image = "docs/blocks/"
path_to_map = "docs/maps/"

# define constants
SQUARE = 50
NUM_OF_TEXTURES = 4
NUM_OF_MAPS = 24 # TODO add more maps
EXIT_CHUNK = 100

# class for the map
class Map():

    def __init__(self, n, m):
        self.display_matrix = [[None for _ in range(15)] for _ in range(25)] # what will be displayed onto the screen
        self.matrix = [[None for _ in range(n)] for _ in range(m)] # TODO make matrix out of block for easy check for collision just a variable
        self.image = [None] * (NUM_OF_TEXTURES + 1)
        self.n = n
        self.m = m
        self.map_coord_x = 0 # TODO maybe delete
        self.map_coord_y = 0 #
        self.level_index = -1
        self.image_cnt = 0 

        # define the matrix
        for i in range(0, n):
            for j in range(0, m):
                block = Block(0, 0, 0)
                self.matrix[i][j] = block

        # load images 
        self.image[0] = pygame.transform.scale(pygame.image.load(path_to_image + "floor.png").convert_alpha(), (SQUARE, SQUARE))
        self.image[1] = pygame.transform.scale(pygame.image.load(path_to_image + "wall.png").convert_alpha(), (SQUARE, SQUARE))
        self.image[4] = pygame.transform.scale(pygame.image.load(path_to_image + "door.png").convert_alpha(), (SQUARE, SQUARE))

        self.make_map()

    def update_display_matrix(self, aux_i, aux_j):
        cnt = 0
        # traverse the display matrix
        for i in range(0, 25, 1):
            for j in range(0, 15, 1):
                if aux_i + i < self.n and aux_j + j < self.m:
                    self.display_matrix[i][j] = self.matrix[aux_i + i][aux_j + j]
        pass
    
    def crete_level(self, level):
        i_index = level % 3 * 25
        j_index = level // 3 * 15
        
        for i in range(0, 5, 1):
            for j in range(0, 3, 1):
                # generate a random number to select a map chunk
                random_integer = random.randint(1, NUM_OF_MAPS)
                    
                if i == 4 and j == 2:
                    random_integer = EXIT_CHUNK
                    # get the info from the file
                vect = self.read_file(path_to_map + str(random_integer))
                    
                print(str(i_index + i * 5) + " " + str(j_index + j * 5))
                self.populate_matrix(i_index + i * 5, j_index + j * 5, vect)


    # method that puts the map on screen
    def show_map(self, screen, result):
        # change the level if the player exited
        if result == True:
            self.level_index += 1
            self.update_display_matrix(self.level_index % 3 * 25, self.level_index // 3 * 15)

        for i in range(0, 25, 1):
            for j in range(0, 15, 1):
                screen.blit(self.display_matrix[i][j].block, (i * SQUARE, j * SQUARE))
                self.display_matrix[i][j].rect = pygame.Rect(i * SQUARE, j * SQUARE, SQUARE, SQUARE)
                self.display_matrix[i][j].x = i * SQUARE
                self.display_matrix[i][j].y = j * SQUARE
        
    
    # combines the files 
    def make_map(self):
        for i in range(0, self.n // 5, 1):
            for j in range(0,  self.m // 5, 1):
                # generate a random number to select a map chunk
                random_integer = random.randint(1, NUM_OF_MAPS)
                
                if (i + 1) % 5 == 0 and (j + 1) % 3 == 0:
                    random_integer = EXIT_CHUNK
                    #random_integer = EXIT_CHUNK
                # get the info from the file
                vect = self.read_file(path_to_map + str(random_integer))
                
                self.populate_matrix(i * 5, j * 5, vect)
        
        self.modify_matrix()   
        self.update_display_matrix(0, 0)         

    def modify_matrix(self):
        # verify the map
        while self.verify_map_logic() == False:
            pass

    def change_chunk(self, i, j):
        # generate a random number to select a map chunk
        random_integer = random.randint(1, NUM_OF_MAPS)
        # get the info from the file
        vect = self.read_file(path_to_map + str(random_integer))
        # repeat the step until it is correct
        self.populate_matrix(i * 5, j * 5, vect)

    # method that checks that you can pass from a chunk to another
    def verify_map_logic(self):
        for level in range(0, 15, 1):
            i_index = level % 3 * 25
            j_index = level // 3 * 15

            # check that on the first column until i th line there are only 1s
            for i in range(i_index, i_index + 25, 1):
                if self.matrix[i][j_index].block_type != 1:
                    self.change_chunk(i // 5, j_index // 5)
                    return False

            # check that on the first row column until j th column there are only 1s
            for i in range(j_index, j_index + 15, 1):
                if self.matrix[i_index][i].block_type != 1:
                    self.change_chunk(i_index // 5, i // 5)
                    return False

            # check that on the last column until i th line there are only 1s
            for i in range(i_index, i_index + 25, 1):
                if self.matrix[i][j_index + 15 - 1].block_type != 1:
                    self.change_chunk(i // 5, (j_index + 15 - 1) // 5)
                    return False
            # check that on the last row until j th column there are only 1s
            for i in range(j_index, j_index + 15, 1):
                if self.matrix[i_index + 25 - 1][i].block_type != 1:
                    self.change_chunk((i_index + 25 - 1) // 5, i // 5)
                    return False
                

            start_x, start_y = i_index + 2, j_index + 2
            end_x, end_y = i_index + 25 - 2, j_index + 15 - 2

            # check if there is a path to the exit
            if not self.has_path(start_x, start_y, end_x, end_y):
                self.crete_level(level)
                return False

        return True
    
    def populate_matrix(self, i_start, j_start, values):
        cnt = 0
        # populate the matrix
        for i in range(i_start, i_start + 5, 1):
            for j in range(j_start, j_start + 5, 1):
                self.matrix[i][j].block_type = values[cnt] # change the block type
                self.matrix[i][j].block.blit(self.image[values[cnt]], (0, 0))

                cnt += 1

    # read from the text file 
    def read_file(self, path):

        # open the file for reading
        with open(path, 'r') as file:
            # read the first line
            first_line = file.readline()

        # number of blocks in the file
        n = 5 * 5  
        elements = first_line.split()[:n] 

        # convert to ints
        int_elements = [int(element) for element in elements]  

        # return the array
        return int_elements

    # function that checks if there is a path to the exit on each level
    def has_path(self, start_x, start_y, end_x, end_y):
        # init the visited array
        visited = [[False for _ in range(self.n)] for _ in range(self.m)]
        q = Queue()

        # add intot the queue
        q.put((start_x, start_y))
        visited[start_x][start_y] = True

        while not q.empty():
            x, y = q.get()

            # check if the exit has been reached
            if x == end_x and y == end_y:
                return True
            # define the directions
            dx = [0, 0, -1, 1]
            dy = [-1, 1, 0, 0]

            for i in range(4):
                nx, ny = x + dx[i], y + dy[i]

                if 0 <= nx < end_x + 2 and 0 <= ny < end_y + 2 and not visited[nx][ny] and self.matrix[nx][ny].block_type == 0:
                    q.put((nx, ny))
                    visited[nx][ny] = True

        return False

