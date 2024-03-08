import pygame

# define constants
NUM_FRAMES = 4
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

SQUARE = 50

class Animate:

    # format for image "name_i"
    def __init__(self,image, state, screen):
        self.image_cnt = 1 # set the first frame
        self.image = [None] * (NUM_FRAMES * 4 + 1)  # initialize as a list of None
        self.state = state # set the state
        self.square_surface = pygame.Surface((26, 38), pygame.SRCALPHA) # create the square
        self.screen = screen # save the screen

        # get all the images 
        for i in range(1, NUM_FRAMES * 4 + 1):
            self.image[i] = pygame.image.load(self.make_string(i, image)).convert_alpha()

    def animate(self, state):
        # find the next image
        self.find_next_state(state)

        # modify the image on screen
        # fill with trasnparent background
        self.square_surface.fill((255, 255, 255, 0))

        # add the texture
        self.square_surface.blit(self.image[self.image_cnt], (0, 0))


    # get the next frame
    def next_frame(self):
        number = self.image_cnt % 4# image index from 0 to 3

        # if the last frame
        if (number == 0):
            self.image_cnt -= 3# reset the frame

        else: 
            self.image_cnt += 1 


    def find_next_state(self, state):
        if (self.state == state):
            self.next_frame()
        else:
            # change the animation for another direction
            self.state = state
            self.image_cnt = 4 * self.return_value() - 3

    # returns the value asociated to the state
    def return_value(self):
        if (self.state == "UP"):
            return UP
        elif (self.state == "DOWN"):
            return DOWN
        elif (self.state == "LEFT"):
            return LEFT
        return RIGHT

    def make_string(self, i, image):
        # returns the name of the image
        return image + "" + str(i) + ".png"
