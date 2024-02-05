from enum import Enum
from typing import List, Dict
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
    def prune_directions(self) -> None:
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

    def check_contradiction(self, choices: List[int]) -> bool:
        return len(self.numbers.difference(choices)) == 0

    def collapse(self, cage_size: int) -> (int, Dict[Direction, bool], List[int], Dict[Direction, bool]):
        # roll a state out of valid ones
        numbers_before_collapse = self.numbers.copy()
        directions_before_collapse = self.direction_connections.copy()

        number = np.random.choice(list(self.numbers))
        self.numbers = {number}

        # roll connections
        unlocked_directions = [direction for direction, flag in self.direction_connections.items() if not flag]
        prob = 1/(2**cage_size)

        for direction in unlocked_directions:
            self.direction_connections[direction] = np.random.choice([True, False], p=[prob, 1 - prob])
        
        self.collapsed = True
        return number, self.direction_connections, numbers_before_collapse, directions_before_collapse
