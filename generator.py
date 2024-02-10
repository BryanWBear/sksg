# copied from https://github.com/norvig/pytudes/blob/main/ipynb/Sudoku.ipynb

import random
import re
from enum import Enum
from typing import List, Dict
import numpy as np


class Direction(Enum):
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    UP = 'UP'
    DOWN = 'DOWN'


DigitSet = str  # e.g. '123'
Square   = str  # e.g. 'A9'
Picture  = str  # e.g. "53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79"
Grid     = dict # E.g. {'A9': '123', ...}, a dict  of {Square: DigitSet}
Fail     = Grid() # The empty Grid is used to indicate failure to find a solution


def cross(A, B) -> tuple:
    "Cross product of strings in A and strings in B."
    return tuple(a + b for a in A for b in B)


digits    = '123456789'
rows      = digits
cols      = digits
squares   = cross(rows, cols)
all_boxes = [cross(rs, cs)  for rs in ('123','456','789') for cs in ('123','456','789')]
all_units = [cross(rows, c) for c in cols] + [cross(r, cols) for r in rows] + all_boxes
units     = {s: tuple(u for u in all_units if s in u) for s in squares}
peers     = {s: set().union(*units[s]) - {s} for s in squares}


def is_solution(solution: Grid, puzzle: Grid) -> bool:
    "Is this proposed solution to the puzzle actually valid?"
    return (solution is not Fail and
            all(solution[s] == puzzle[s] for s in squares if len(puzzle[s]) == 1) and
            all({solution[s] for s in unit} == set(digits) for unit in all_units))


def fill(grid, s, d) -> Grid:
    """Eliminate all the other digits (except d) from grid[s]."""
    if grid[s] == d or all(eliminate(grid, s, d2) for d2 in grid[s] if d2 != d):
        return grid
    else:
        return Fail


def eliminate(grid, s, d) -> Grid:
    """Eliminate d from grid[s]; implement the two constraint propagation strategies."""
    if d not in grid[s]:
        return grid        ## Already eliminated
    grid[s] = grid[s].replace(d, '')
    if not grid[s]:
        return Fail        ## Fail: no legal digit left
    elif len(grid[s]) == 1:
        # 1. If a square has only one possible digit, then eliminate that digit from the square's peers.
        d2 = grid[s]
        if not all(eliminate(grid, s2, d2) for s2 in peers[s]):
            return Fail    ## Fail: can't eliminate d2 from some square
    for u in units[s]:
        dplaces = [s for s in u if d in grid[s]]
        # 2. If a unit has only one possible square that can hold a digit, then fill the square with the digit.
        if not dplaces or (len(dplaces) == 1 and not fill(grid, dplaces[0], d)):
            return Fail    ## Fail: no place in u for d
    return grid


def search(grid) -> Grid:
    "Depth-first search with constraint propagation (`fill`) to find a solution."
    if grid is Fail:
        return Fail
    unfilled = [s for s in squares if len(grid[s]) > 1]
    if not unfilled:
        return grid
    random.shuffle(unfilled)
    s = min(unfilled, key=lambda s: len(grid[s]))
    nums = grid[s]
    nums = [int(x) for x in list(nums)]
    random.shuffle(nums)
    for d in ''.join([str(x) for x in nums]):
        solution = search(fill(grid.copy(), s, d))
        if solution:
            return solution
    return Fail


def constrain(grid) -> Grid:
    "Propagate constraints on a copy of grid to yield a new constrained Grid."
    constrained: Grid = {s: digits for s in squares}
    for s in grid:
        d = grid[s]
        if len(d) == 1:
            fill(constrained, s, d)
    return constrained


def solve(puzzles, verbose=True):
    "Solve and verify each puzzle, and if `verbose`, print puzzle and solution."
    sep = '    '
    for puzzle in puzzles:
        solution = search(constrain(puzzle))
        assert is_solution(solution, puzzle)
    return solution


def parse(picture) -> Grid:
    """Convert a Picture to a Grid."""
    vals = re.findall(r"[.1-9]|[{][1-9]+[}]", picture)
    assert len(vals) == 81
    return {s: digits if v == '.' else re.sub(r"[{}]", '', v)
            for s, v in zip(squares, vals)}


def get_neighbors(tile):
    row, column = tile
    neighbors = [(row + 1, column), (row - 1, column), (row, column + 1), (row, column - 1)]
    return [neighbor for neighbor in neighbors if neighbor[0] >= 1 and neighbor[0] <= 9 and
            neighbor[1] >= 1 and neighbor[1] <= 9]


def get_neighbors_in_partition(tile, tile_to_partition):
    neighbors = get_neighbors(tile)
    return [neighbor for neighbor in neighbors if neighbor in tile_to_partition]


def is_cage_valid(board, partition):
    visited = set()
    for tile in partition:
        if board[tile] in visited:
            return False
        visited.add(board[tile])

    return True


def partition_board(board):
    num_partitions = 34
    tile_to_partition = {}
    tiles = list(board.keys())
    random.shuffle(tiles)
    partitions = {i: [] for i in range(num_partitions)}

    # initialize partition
    for i in range(num_partitions):
        tile_to_partition[tiles[i]] = i
        partitions[i].append(tiles[i])

    while len(tile_to_partition) < 81:
        for tile in tiles:
            if tile in tile_to_partition:
                continue
            neighbors = get_neighbors_in_partition(tile, tile_to_partition)
            if len(neighbors) == 0:
                continue
            neighbor = random.choice(neighbors)
            neighbor_partition = tile_to_partition[neighbor]
            tile_to_partition[tile] = neighbor_partition
            partitions[neighbor_partition].append(tile)
            if not is_cage_valid(board, partitions[neighbor_partition]):
                return False

    return partitions


class Tile:
    def __init__(self, tile_coords, directions, cage, number):
        self.tile_coords = tile_coords
        self.directions = directions
        self.cage = cage
        self.number = int(number)


def get_neighbor_directions(tile, partition):
    row, column = tile
    directions = set()
    if (row + 1, column) in partition:
        directions.add(Direction.DOWN)
    if (row - 1, column) in partition:
        directions.add(Direction.UP)
    if (row, column + 1) in partition:
        directions.add(Direction.RIGHT)
    if (row, column - 1) in partition:
        directions.add(Direction.LEFT)
    return directions


def generate():
    empty = parse('.' * 81)
    board = solve([empty])
    board = {(int(row), int(col)): board[row + col] for row, col in board}

    partitioned = False
    while not partitioned:
        partitioned = partition_board(board)

    final_board = {}

    for partition in partitioned.values():
        for tile in partition:
            directions = get_neighbor_directions(tile, partition)
            number = board[tile]
            final_board[tile] = Tile(tile, directions, partition, number)

    return final_board, list(partitioned.values())