import math

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def change_x(self, x):
        self.x = x

    def change_y(self, y):
        self.y = y

    # compute the distance
    def distance(self, point):
        return math.sqrt(math.pow(self.x - point.x, 2) + math.pow(self.y - point.y, 2))
    
    