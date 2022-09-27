from utils import *


# HELPERS

def init_grid():
    grid = []

    for i in range(ROWS):
        grid.append([])
        for _ in range(COLS):
            grid[i].append(BG_CANVAS)
    return grid


# CALLED IN EVENT LOOP

def draw_grid(win, grid):
    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            pg.draw.rect(win, pixel, (j * PIXEL_SIZE + PADDING,
                                      i * PIXEL_SIZE + PADDING,
                                      PIXEL_SIZE,
                                      PIXEL_SIZE))
    if DRAW_GRID_LINES:
        for i in range(ROWS + 1):
            pg.draw.line(win, GRAY, (0, i * PIXEL_SIZE), (WIDTH - TOOLBAR_SIZE, i * PIXEL_SIZE))
        for i in range(COLS + 1):
            pg.draw.line(win, GRAY, (i * PIXEL_SIZE, 0), (i * PIXEL_SIZE, HEIGHT))


def draw_bg_img(win):
    for i in range(BG_IMG_X_REPEAT + 1):
        for j in range(BG_IMG_Y_REPEAT + 1):
            win.blit(BG_IMG, (i * BG_IMG.get_width(), j * BG_IMG.get_height()))


def get_row_col_pos(pos):
    x, y = pos

    if x - PADDING < 0 or y - PADDING < 0:
        raise IndexError

    row = (x - PADDING) // PIXEL_SIZE
    col = (y - PADDING) // PIXEL_SIZE

    if row >= ROWS:
        raise IndexError
    if col >= COLS:
        raise IndexError
    return row, col


def erase_row_col_area(grid, row, col):
    grid[col][row] = BG_CANVAS
    for i in range(1, 4):
        grid[col - i][row - i] = BG_CANVAS
        grid[col - i][row + i] = BG_CANVAS
        grid[col + i][row - i] = BG_CANVAS
        grid[col + i][row + i] = BG_CANVAS
        grid[col - i][row] = BG_CANVAS
        grid[col][row - i] = BG_CANVAS
        grid[col + i][row] = BG_CANVAS
        grid[col][row + i] = BG_CANVAS


def draw_bg(win):
    win.fill(BG_COLOR)
    draw_bg_img(win)


def draw_chat_layout(win, text_surface, active):
    pg.draw.rect(win, BG_CHAT, CHAT_RECT, border_radius=5)
    pg.draw.rect(win, BLACK, CHAT_RECT, width=1, border_radius=5)

    border_padding = 2
    pg.draw.rect(win, WHITE, INPUT_REC)
    pg.draw.rect(win, YELLOW if active else BLACK,
                 (
                     INPUT_REC.x - border_padding,
                     INPUT_REC.y - border_padding,
                     INPUT_REC.w + 2 * border_padding,
                     INPUT_REC.h + 2 * border_padding,
                 ),
                 width=2, border_radius=2)


def do_input_tick(win, text_surface):
    pg.draw.line(win, BLACK,
                 (
                     CHAT_RECT.x + TEXT_PADDING + text_surface.get_width() + 1,
                     CHAT_RECT.y + CHAT_RECT.height - text_surface.get_height() - TEXT_PADDING + 3,
                 ),
                 (
                     CHAT_RECT.x + TEXT_PADDING + text_surface.get_width() + 1,
                     CHAT_RECT.y + CHAT_RECT.height - text_surface.get_height() - TEXT_PADDING + text_surface.get_height() - 3
                 ))


def draw_chat(win, active, font, chat: Chat, make_input_tick):
    text_surface = font.render(chat.current_text, True, BLACK)
    draw_chat_layout(win, text_surface, active)
    win.blit(text_surface, (CHAT_RECT.x + TEXT_PADDING,
                            CHAT_RECT.y + CHAT_RECT.height - text_surface.get_height() - TEXT_PADDING))
    if make_input_tick:
        do_input_tick(win, text_surface)


def draw_canvas(win, grid):
    draw_grid(win, grid)
