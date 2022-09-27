import pygame as pg

pg.init()
pg.font.init()

pg.key.set_repeat(500, 30)
pg.display.set_caption("Draw and Guess!")

###############################################################
#                       DEFAULT VALUES                        #
###############################################################
# COLORS
BLACK = (0, 0, 0)
GRAY = (140, 140, 140)
WHITE = (255, 255, 255)
RED = (255, 87, 51)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (239, 193, 83)
BG_COLOR = (36, 100, 242)
BG_CHAT = (80, 80, 80, 127)
BG_TIMER = (17, 48, 106)
BG_CANVAS = WHITE

# WINDOW
FPS = 60
WIDTH, HEIGHT = 1100, 600
PADDING = 50

# CANVAS
ROWS = COLS = 100

# CHAT
INPUT_TICK_RATE = 500  # in ms
TEXT_PADDING = 10
MAX_CHAR = 28
DEFAULT_FONT_SIZE = 16

# TIMER
TIMER_HEIGHT = 15
TIMER_DUR = 60000  # in ms


###############################################################
#                   STATIC CALCULATIONS                       #
###############################################################

def get_font(size):
    return pg.font.SysFont(
        # './resources/fonts/JetBrains Mono Regular Nerd Font Complete.ttf',
        'arial',
        size,
    )


TOOLBAR_SIZE = abs(WIDTH - HEIGHT)

PIXEL_SIZE = (min(WIDTH, HEIGHT) - 2 * PADDING) // COLS

DRAW_GRID_LINES = False

BG_IMG = pg.image.load("./resources/images/texture.png")
BG_IMG_X_REPEAT = WIDTH // BG_IMG.get_width()
BG_IMG_Y_REPEAT = HEIGHT // BG_IMG.get_height()

CHAT_RECT = pg.Rect(WIDTH - TOOLBAR_SIZE + PADDING,
                    PADDING,
                    TOOLBAR_SIZE - 2 * PADDING,
                    HEIGHT - 2 * PADDING)

INPUT_REC = pg.Rect(
    CHAT_RECT.x + TEXT_PADDING,
    CHAT_RECT.y + CHAT_RECT.height - get_font(DEFAULT_FONT_SIZE).get_height() - TEXT_PADDING,
    CHAT_RECT.w - 2 * TEXT_PADDING,
    get_font(DEFAULT_FONT_SIZE).get_height()
)

TIMER_RECT = pg.Rect(PADDING, (PADDING - TIMER_HEIGHT) // 2, WIDTH - 2 * PADDING, TIMER_HEIGHT)
