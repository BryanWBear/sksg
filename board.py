from tile import Tile, Direction
from cage import Cage
from typing import List
import numpy as np
import copy

class Board:
    def __init__(self, board_size=4) -> None:
        self.tiles = {}
        self.tile_to_cage_mapping = {}
        self.board_size = board_size

        # assume that i = row, j = column, and that (0, 0) is the top left corner of the grid.
        for i in range(board_size):
            for j in range(board_size):
                self.tiles[(i, j)] = Tile(i, j, board_size)
                self.tile_to_cage_mapping[(i, j)] = Cage((i, j))
        

    def get_tiles(self) -> List[Tile]:
        return list(self.tiles.values())
    
    def get_row_tiles(self, tile_idx: (int, int)) -> List[Tile]:
        row, column = tile_idx
        return [self.tiles[(i, column)] for i in range(self.board_size) if i != row]
    
    def get_column_tiles(self, tile_idx: (int, int)) -> List[Tile]:
        row, column = tile_idx
        return [self.tiles[(row, i)] for i in range(self.board_size) if i != column]
    
    def get_cage_tiles(self, initial_tile_idx) -> List[Tile]:
        tile_idxs = self.tile_to_cage_mapping[initial_tile_idx].tiles
        return [self.tiles[tile_idx] for tile_idx in tile_idxs if tile_idx != initial_tile_idx]
    
    def get_uncollapsed_tiles(self) -> List[Tile]:
        return [tile for tile in self.tiles.values() if not tile.collapsed]
    
    def get_tile_coords(self) -> List[Tile]:
        return list(self.tiles.keys())
    
    def get_collapse_candidate(self) -> Tile:
        # can be more efficient
        min_states = min(tile.valid_numbers for tile in self.get_uncollapsed_tiles())
        candidate = np.random.choice([tile for tile in self.get_uncollapsed_tiles() if tile.valid_numbers == min_states])
        return candidate
    
    def combine_two_cages(self, tile_idx: (int, int), new_idx: (int, int)):
        new_row, new_col = new_idx
        if new_row >= self.board_size or new_row < 0 or new_col >= self.board_size or new_row < 0:
            return
        new_cage = self.tile_to_cage_mapping[new_idx]
        old_cage = self.tile_to_cage_mapping[tile_idx]
        old_cage.merge(new_cage)
        for tile in old_cage.tiles:
            self.tile_to_cage_mapping[tile] = old_cage
    
    def connect_cages(self, tile_idx: (int, int), directions):
        for direction in directions:
            if not directions[direction]:
                continue
            row, column = tile_idx
            if direction == Direction.DOWN:
                new_idx = (row + 1, column)
            elif direction == Direction.LEFT:
                new_idx = (row, column - 1)
            elif direction == Direction.RIGHT:
                new_idx = (row, column + 1)
            elif direction == Direction.UP:
                new_idx = (row - 1, column)
            new_cage_copy = copy.deepcopy(self.tile_to_cage_mapping[new_idx])
            old_cage_copy = copy.deepcopy(self.tile_to_cage_mapping[tile_idx])
            self.combine_two_cages(tile_idx, new_idx)

            return new_cage_copy, old_cage_copy
        return None, None