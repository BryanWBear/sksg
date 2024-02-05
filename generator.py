from board import Board
from tile import Tile

MAX_NUM_CONTRADICTIONS = 144  # kind of a hack, 9 * 16 for a 9x9 sudoku.


class BoardGenerator:
    def __init__(self, board_size: int):
        self.board = Board(board_size=board_size)

    def is_board_done(self) -> bool:
        return all(tile.collapsed for tile in self.board.get_tiles())

    @staticmethod
    def is_contradiction(tile: Tile) -> bool:
        return tile.valid_numbers == 0

    def generate(self):
        collapse_count = 0
        while True:
            if self.is_board_done():
                print('we are done.')
                break
            if any(self.is_contradiction(tile) for tile in self.board.get_tiles()):
                print(f'we failed at {collapse_count} tiles placed.')
                break

            collapse_candidate = self.board.get_collapse_candidate()
            collapse_candidate_idx = (collapse_candidate.position_x, collapse_candidate.position_y)
            cage_size = len(self.board.tile_to_cage_mapping[collapse_candidate_idx].tiles)

            for _ in range(MAX_NUM_CONTRADICTIONS):
                (number, directions,
                 numbers_before_collapse, directions_before_collapse) = collapse_candidate.collapse(cage_size)

                new_cage_copy, old_cage_copy = self.board.connect_cages(collapse_candidate_idx, directions)

                row_tiles = self.board.get_row_tiles(collapse_candidate_idx)
                column_tiles = self.board.get_column_tiles(collapse_candidate_idx)
                cage_tiles = self.board.get_cage_tiles(collapse_candidate_idx)

                tiles = row_tiles + column_tiles + cage_tiles

                # backtracking
                if any(tile.check_contradiction([number]) for tile in tiles):
                    # reset collapsed cell state
                    collapse_candidate.numbers = numbers_before_collapse
                    collapse_candidate.direction_connections = directions_before_collapse
                    collapse_candidate.collapsed = False

                    # reset connected cages
                    if new_cage_copy and old_cage_copy:
                        for tile in new_cage_copy.tiles:
                            self.board.tile_to_cage_mapping[tile] = new_cage_copy

                        for tile in old_cage_copy.tiles:
                            self.board.tile_to_cage_mapping[tile] = old_cage_copy
                else:
                    for tile in tiles:
                        tile.eliminate([number])
                    collapse_count += 1
                    break

    



