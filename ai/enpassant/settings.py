
b_height =512
b_width = 580
b_dimensions = 8
b_size = b_height//b_dimensions
FPS = 15
TILE_SIZE = 64
SCREEN_WIDTH = b_width
SCREEN_HEIGHT = b_height
BOARD_SIZE = b_size * 8
BOARD_X = (SCREEN_WIDTH-BOARD_SIZE)//2
BOARD_Y = int((SCREEN_HEIGHT / 2) - (BOARD_SIZE / 2))
IMG_SCALE = (b_size, b_size)

# Basic colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game colors
SMALL_TEXT_COLOR = (241, 250, 238)
LARGE_TEXT_COLOR = (230, 57, 70)
BG_COLOR = (29, 53, 87)
BG_COLOR_LIGHT = (70, 70, 70)
TILE_COLOR_LIGHT = (241, 250, 238)
TILE_COLOR_DARK = (69, 123, 157)
HIGHLIGHT_COLOR = (51, 153, 255)

# Create screen


# MinMax
DEPTH=8
THRESHHOLD=4
SCORE=50000

# Converts 8x8 grid locations to pixel coordinates
def to_coords(x, y):
    return BOARD_X + x * TILE_SIZE, BOARD_Y + y * TILE_SIZE