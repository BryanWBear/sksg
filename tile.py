from enum import Enum
from typing import List
import numpy as np

class Direction(Enum):
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    UP = 'UP'
    DOWN = 'DOWN'

class Tile:
    def __init__(self, position_x, position_y, board_size) -> None:
        self.position_x = position_x
        self.position_y = position_y
        self.board_size = board_size

        self.numbers = set(i for i in range(1, board_size + 1))

        self.direction_connections = {
            Direction.LEFT: False,
            Direction.RIGHT: False,
            Direction.UP: False,
            Direction.DOWN: False
        }

        self.prune_directions()

        self.collapsed = False
        self.valid_numbers = len(self.numbers)


    # remove invalid directions for corner and edge tiles
    def prune_directions(self):
        if self.position_x == 0:
            del self.direction_connections[Direction.UP]
        if self.position_y == 0:
            del self.direction_connections[Direction.LEFT]
        if self.position_x == self.board_size - 1:
            del self.direction_connections[Direction.DOWN]
        if self.position_y == self.board_size - 1:
            del self.direction_connections[Direction.RIGHT]


    def eliminate(self, choices: List[int]) -> None:
        self.numbers = self.numbers.difference(choices)
        self.valid_numbers = len(self.numbers)


    def collapse(self):
        # roll a state out of valid ones
        number = np.random.choice(list(self.numbers))
        self.numbers = set([number])

        # roll connections
        unlocked_directions = [direction for direction, flag in self.direction_connections.items() if not flag]
        for direction in unlocked_directions:
            self.direction_connections[direction] = np.random.choice([True, False])
        
        self.collapsed = True
        return number, self.direction_connections

        

