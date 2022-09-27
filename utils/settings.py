import pygame

pygame.init()
pygame.font.init()

pygame.key.set_repeat(500, 30)

###############################################################
#                       DEFAULT VALUES                        #
###############################################################
# COLORS
BLACK = (0, 0, 0)
GRAY = (140, 140, 140)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BG_COLOR = (36, 100, 242)
BG_CANVAS = WHITE

# SHARED
FPS = 60
WIDTH, HEIGHT = 1100, 600
PADDING = 50

# CANVAS
ROWS = COLS = 100

#  CHAT
TEXT_PADDING = 6
MAX_CHAR = 32

###############################################################
#                   STATIC CALCULATIONS                       #
###############################################################

TOOLBAR_SIZE = abs(WIDTH - HEIGHT)

PIXEL_SIZE = (min(WIDTH, HEIGHT) - 2 * PADDING) // COLS

DRAW_GRID_LINES = False

BG_IMG = pygame.image.load("./resources/images/texture.png")
BG_IMG_X_REPEAT = WIDTH // BG_IMG.get_width()
BG_IMG_Y_REPEAT = HEIGHT // BG_IMG.get_height()


def get_font(size):
    return pygame.font.SysFont(
        './resources/fonts/JetBrains Mono Regular Nerd Font Complete.ttf',
        size,
    )
