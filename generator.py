from board import Board
from tile import Tile


def is_board_done(board: Board) -> bool:
    return all(tile.collapsed for tile in board.get_tiles())


def is_contradiction(tile: Tile) -> bool:
    return tile.valid_numbers == 0



if __name__ == '__main__':
    board = Board()
    while True:
        if is_board_done(board):
            print('we are done.')
            break
        if any(is_contradiction(tile) for tile in board.get_tiles()):
            print('we failed.')
            break

        collapse_candidate = board.get_collapse_candidate()
        collapse_candidate_idx = (collapse_candidate.position_x, collapse_candidate.position_y)

        number, directions = collapse_candidate.collapse()

        board.connect_cages(collapse_candidate_idx, directions)

        row_tiles = board.get_row_tiles(collapse_candidate_idx)
        column_tiles = board.get_column_tiles(collapse_candidate_idx)
        cage_tiles = board.get_cage_tiles(collapse_candidate_idx)

        for tile in row_tiles + column_tiles + cage_tiles:
            tile.eliminate([number])
    



