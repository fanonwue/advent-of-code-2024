from typing import List, Tuple
from enum import Enum

ParsedMap = List[List[str]]
Point = Tuple[int, int]

class Direction(Enum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"

class Mode(Enum):
    PART_ONE = 1
    PART_TWO = 2