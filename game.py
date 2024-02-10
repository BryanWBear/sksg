import copy
from pathlib import Path
import cairosvg
import io
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from generator import generate, Direction

DIRECTIONS_TO_IMG_MAP = {
    frozenset([Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]): 'blank.svg',
    frozenset([Direction.LEFT, Direction.RIGHT, Direction.UP]): 'down_only.svg',
    frozenset([Direction.LEFT, Direction.RIGHT, Direction.DOWN]): 'up_only.svg',
    frozenset([Direction.LEFT, Direction.UP, Direction.DOWN]): 'right_only.svg',
    frozenset([Direction.UP, Direction.RIGHT, Direction.DOWN]): 'left_only.svg',
    frozenset([Direction.LEFT, Direction.RIGHT]): 'left_right_missing.svg',
    frozenset([Direction.LEFT, Direction.UP]): 'up_left_missing.svg',
    frozenset([Direction.RIGHT, Direction.DOWN]): 'down_right_missing.svg',
    frozenset([Direction.UP, Direction.DOWN]): 'up_down_missing.svg',
    frozenset([Direction.RIGHT, Direction.UP]): 'up_right_missing.svg',
    frozenset([Direction.DOWN, Direction.LEFT]): 'down_left_missing.svg',
    frozenset([Direction.DOWN]): 'down_missing.svg',
    frozenset([Direction.RIGHT]): 'right_missing.svg',
    frozenset([Direction.UP]): 'up_missing.svg',
    frozenset([Direction.LEFT]): 'left_missing.svg',
    frozenset([]): 'full.svg',
}

# Specify the path to your SVG file
ASSETS_PATH = Path(__file__).resolve().parent/'assets'


def load_pil(filename: str) -> Image:
    with open(ASSETS_PATH/filename, 'r') as file:
        svg_content = file.read()

    png_bytes = cairosvg.svg2png(svg_content)

    # Open the PNG image as a PIL Image
    pil_image = Image.open(io.BytesIO(png_bytes))
    return pil_image


def get_top_left_tile(cage_tiles) -> (int, int):
    x_min = min([t_x for t_x, t_y in cage_tiles])
    top_tiles = [t for t in cage_tiles if t[0] == x_min]
    return min(top_tiles, key=lambda t: t[1])


def draw_cage_sum(cage_sum, img: Image) -> Image:
    img_copy = copy.deepcopy(img)
    draw = ImageDraw.Draw(img_copy)

    # Define the text to draw
    number = cage_sum

    # Define the position to draw the text (top-left corner)
    text_position = (25, 25)

    # Define the font style (replace 'arial.ttf' with the path to your font file)
    font = ImageFont.truetype(str(ASSETS_PATH/"Comic Sans MS.ttf"), 32)

    # Draw the number on the image
    draw.text(text_position, str(number), fill="black", font=font)

    return img_copy


def get_cage_sum(cage_tiles, board) -> int:
    return sum(board[tile].number for tile in cage_tiles)


DIRECTIONS_TO_IMG_MAP = {key: load_pil(filename) for key, filename in DIRECTIONS_TO_IMG_MAP.items()}

board, cages = generate()

rows = []
for i in range(1, 10):
    row = []
    for j in range(1, 10):
        tile = board[(i, j)]
        directions_set = frozenset(tile.directions)
        row.append(DIRECTIONS_TO_IMG_MAP[directions_set])
    rows.append(row)

for cage in cages:
    cage_sum = get_cage_sum(cage, board)
    top_left = get_top_left_tile(cage)
    i, j = top_left
    i -= 1
    j -= 1
    rows[i][j] = draw_cage_sum(cage_sum, rows[i][j])

rows = [np.concatenate(row, axis=1) for row in rows]
board_image = Image.fromarray(np.concatenate(rows))

background = Image.new("L", board_image.size, 255)
background.paste(board_image, (0, 0), board_image)
background.save('board.png')
