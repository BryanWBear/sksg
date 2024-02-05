from pathlib import Path
import cairosvg
import io
from PIL import Image
import numpy as np
from tile import Direction

DIRECTIONS_TO_IMG_MAP = {
    frozenset([Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]): 'blank.svg',
    frozenset([Direction.LEFT, Direction.RIGHT, Direction.UP]): 'down_missing.svg',
    frozenset([Direction.LEFT, Direction.RIGHT, Direction.DOWN]): 'up_missing.svg',
    frozenset([Direction.LEFT, Direction.UP, Direction.DOWN]): 'right_missing.svg',
    frozenset([Direction.UP, Direction.RIGHT, Direction.DOWN]): 'left_missing.svg',
    frozenset([Direction.LEFT, Direction.RIGHT]): 'up_down_missing.svg',
    frozenset([Direction.LEFT, Direction.UP]): 'down_right_missing.svg',
    frozenset([Direction.RIGHT, Direction.DOWN]): 'up_left_missing.svg',
    frozenset([Direction.UP, Direction.DOWN]): 'left_right_missing.svg',
    frozenset([Direction.RIGHT, Direction.UP]): 'down_left_missing.svg',
    frozenset([Direction.DOWN, Direction.RIGHT]): 'up_right_missing.svg',
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


DIRECTIONS_TO_IMG_MAP = {key: load_pil(filename) for key, filename in DIRECTIONS_TO_IMG_MAP.items()}

# Create a 3x3 grid of square images
# grid_rows = 3
# grid_cols = 3
# image_size = 200
#
# im_array = np.array(pil_image)
# new_im = Image.fromarray(np.concatenate([im_array, im_array]))
# background = Image.new("L", new_im.size, 255)
# background.paste(new_im, (0, 0), new_im)
# background.save('test.png')