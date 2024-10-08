from definitions import *

import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg

pg.init()
pg.font.init()

pg.key.set_repeat(500, 30)  # chat input - deleting, edit, etc

###############################################################
#                       DEFAULT VALUES                        #
###############################################################
# COLOR DEFINITIONS
BLACK = (0, 0, 0)
GRAY = (175, 175, 175)
LIGHT_GRAY = (211, 211, 211)
WHITE = (255, 255, 255)
RED = (255, 87, 51)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (239, 193, 83)
ORANGE = (255, 127, 80)

# GUI COLORS
BG_COLOR = (36, 100, 242)
BG_CHAT = (80, 80, 80)
BG_TIMER = (17, 48, 106)
BG_CANVAS = WHITE
DEFAULT_TEXT_COLOR = WHITE
SERVER_MESSAGE_COLOR = RED
CORRECT_ANSWER_COLOR = GREEN

# WINDOW
FPS = 30
WIDTH, HEIGHT = 1100, 600
PADDING = 50

# CANVAS
DRAW_GRID_LINES = True

# CHAT
INPUT_TICK_RATE = 500  # in ms
CHAT_INPUT_BG_PADDING = 10
TEXT_PADDING = 2
CHAT_BORDER_RADIUS = 5
CHAT_BORDER_WIDTH = 1
DEFAULT_FONT_SIZE = 16
CHAT_ALPHA = 128
HIST_BUFFER_SIZE = 25

# PLAYER LIST
STATUS_CIRCLE_RADIUS = 5
STATUS_CIRCLE_DIAMETER = STATUS_CIRCLE_RADIUS * 2

# BUTTONS
BUTTON_RADIUS = 3

# TIMER
TIMER_HEIGHT = 15

ROUND_DUR_MS = ROUND_DUR_SEC * 1000  # in ms

# SOCKETS
TIMEOUT_SEC = 3


###############################################################
#                   STATIC CALCULATIONS                       #
###############################################################

def get_font(size):
    return pg.font.SysFont(
        'arial',
        size,
    )


CANVAS_SIZE = ROWS * COLS
CANVAS_SIZE_SERIALIZED = int(CANVAS_SIZE / 8 + (1 if CANVAS_SIZE % 8 else 0))

WIN = pg.display.set_mode((WIDTH, HEIGHT))
FONT = get_font(DEFAULT_FONT_SIZE)
FONT_HEIGHT = FONT.get_height()
HISTORY_CHAT_INPUT_PADDING = FONT_HEIGHT * .5

TOOLBAR_SIZE = abs(WIDTH - HEIGHT)

PIXEL_SIZE = (min(WIDTH, HEIGHT) - 2 * PADDING) // COLS

BG_IMG = pg.image.load("./resources/images/texture.png")
BG_IMG_X_REPEAT = WIDTH // BG_IMG.get_width()
BG_IMG_Y_REPEAT = HEIGHT // BG_IMG.get_height()

CHAT_RECT = pg.Rect(WIDTH - TOOLBAR_SIZE + PADDING,
                    PADDING,
                    TOOLBAR_SIZE - 2 * PADDING,
                    HEIGHT - 2 * PADDING)

CHAT_SURF = pg.Surface((CHAT_RECT.w, CHAT_RECT.h))
CHAT_SURF.set_alpha(CHAT_ALPHA)
CHAT_SURF.fill(BG_CHAT)

INPUT_REC = pg.Rect(
    CHAT_RECT.x + CHAT_INPUT_BG_PADDING,
    CHAT_RECT.y + CHAT_RECT.h - FONT_HEIGHT - CHAT_INPUT_BG_PADDING,
    CHAT_RECT.w - 2 * CHAT_INPUT_BG_PADDING,
    FONT_HEIGHT)

TIMER_RECT = pg.Rect(PADDING, (PADDING - TIMER_HEIGHT) // 2, WIDTH - 2 * PADDING, TIMER_HEIGHT)

__x_padding = 4
__y_padding = 2
__btn_size = 25
PLAYER_LIST_BTN = pg.Rect(CHAT_RECT.x + CHAT_RECT.w + __x_padding,
                          CHAT_RECT.y + __y_padding,
                          __btn_size,
                          __btn_size)

__btn_size *= 0.8
PLAYER_LIST_IMG_POS = pg.Rect(0, 0, __btn_size, __btn_size)
PLAYER_LIST_IMG_POS.center = PLAYER_LIST_BTN.center
PLAYER_LIST_IMG = pg.image.load("./resources/images/player-list.webp")
PLAYER_LIST_IMG = pg.transform.scale(PLAYER_LIST_IMG, (PLAYER_LIST_IMG_POS.w, PLAYER_LIST_IMG_POS.h))

__player_list_padding = 5
PLAYER_LIST_RECT = pg.Rect(CHAT_RECT.x + CHAT_RECT.w * .5 - __player_list_padding,
                           CHAT_RECT.y + __player_list_padding,
                           CHAT_RECT.w * .5,
                           0)
