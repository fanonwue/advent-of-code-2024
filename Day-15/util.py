from typing import List, Tuple
from enum import Enum

ParsedMap = List[List[str]]
Point = Tuple[int, int]

class Direction(Enum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"

    def is_vertical(self):
        return self in [Direction.UP, Direction.DOWN]

    def is_horizontal(self):
        return self in [Direction.LEFT, Direction.RIGHT]

class Mode(Enum):
    PART_ONE = 1
    PART_TWO = 2