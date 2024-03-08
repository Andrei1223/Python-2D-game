import pygame

SQUARE = 50

class Block:

    def __init__(self, x, y, block_type):
        self.x = x
        self.y = y
        self.block_type = block_type
        # create a surface for the block
        self.block = pygame.Surface((SQUARE, SQUARE), pygame.SRCALPHA)
        self.image = None
        self.rect = pygame.Rect(x, y, SQUARE, SQUARE)
    