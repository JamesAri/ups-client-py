from settings import *
from model import Canvas


def draw_grid(win, canvas: Canvas):
    with canvas.canvas_lock:
        for i, row in enumerate(canvas.grid):
            for j, pixel in enumerate(row):
                pg.draw.rect(win, pixel, (j * PIXEL_SIZE + PADDING,
                                          i * PIXEL_SIZE + PADDING,
                                          PIXEL_SIZE,
                                          PIXEL_SIZE))
    if DRAW_GRID_LINES:
        for i in range(ROWS + 1):
            pg.draw.line(win, GRAY,
                         (
                             PADDING,
                             i * PIXEL_SIZE + PADDING,
                         ),
                         (
                             WIDTH - TOOLBAR_SIZE - PADDING,
                             i * PIXEL_SIZE + PADDING,
                         ))
        for i in range(COLS + 1):
            pg.draw.line(win, GRAY,
                         (
                             i * PIXEL_SIZE + PADDING,
                             PADDING,
                         ),
                         (
                             i * PIXEL_SIZE + PADDING,
                             HEIGHT - PADDING,
                         ))


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


def draw_canvas(win, canvas):
    draw_grid(win, canvas)
