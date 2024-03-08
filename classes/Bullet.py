import pygame

class Bullet:
    def __init__(self, x, y, direction, speed):
        self.x = x
        self.y = y
        self.width = 4
        self.height = 4
        self.speed = speed
        self.color = (255, 0, 0)
        self.direction = direction
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, map, targets):
        result = self.detect_event(map, targets)
        if result != -2:            
            return result

        if self.direction == "UP":
            self.y -= self.speed
        elif self.direction == "DOWN":
            self.y += self.speed
        elif self.direction == "LEFT":
            self.x -= self.speed
        elif self.direction == "RIGHT":
            self.x += self.speed
        
        # update the rectangle
        self.rect.update(self.x, self.y, self.width, self.height)
        
        return result

    def draw(self, screen):
        self.rect = pygame.draw.rect(screen, self.color, self.rect)

    # return -2 if no collision
    # return -1 if collision with a wall
    # return the index of the object if collision with an entity
    def detect_event(self, map, targets):
        for i in range(0, 25, 1):  # TODO check just in the middle for optimization
            for j in range(0, 15, 1):
                block_rect = map.display_matrix[i][j].rect
                if map.display_matrix[i][j].block_type == 1 and self.rect.colliderect(block_rect):
                    return -1  # Collision with a wall
        
        cnt = 0
        for i in range(0, len(targets), 1):
            if self.rect.colliderect(targets[i]):
                return cnt  # collision with an entity
            cnt += 1

        return -2
    
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
