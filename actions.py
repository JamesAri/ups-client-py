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
            pygame.draw.rect(win, pixel, (j * PIXEL_SIZE + PADDING,
                                          i * PIXEL_SIZE + PADDING,
                                          PIXEL_SIZE,
                                          PIXEL_SIZE))
    if DRAW_GRID_LINES:
        for i in range(ROWS + 1):
            pygame.draw.line(win, GRAY, (0, i * PIXEL_SIZE), (WIDTH - TOOLBAR_SIZE, i * PIXEL_SIZE))
        for i in range(COLS + 1):
            pygame.draw.line(win, GRAY, (i * PIXEL_SIZE, 0), (i * PIXEL_SIZE, HEIGHT))


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


def draw_canvas(win, grid):
    draw_grid(win, grid)
