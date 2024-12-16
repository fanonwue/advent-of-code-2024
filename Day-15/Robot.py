from util import Point

class Robot:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def pos(self) -> Point:
        return self.x, self.y

    def move_to(self, pos: Point):
        self.x = pos[0]
        self.y = pos[1]