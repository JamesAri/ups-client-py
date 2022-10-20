import threading
from bitarray import bitarray

from settings import ROWS, COLS, BG_CANVAS, CANVAS_SIZE, BLACK, CANVAS_SIZE_SERIALIZED


class Canvas:
    grid: list = []
    canvas_lock: threading.Lock

    def __init__(self):
        self.__init_grid()
        self.canvas_lock = threading.Lock()

    def __init_grid(self):
        self.grid = [[BG_CANVAS for _ in range(COLS)] for _ in range(ROWS)]

    def clear(self):
        with self.canvas_lock:
            self.__init_grid()

    def unpack_and_set(self, serialized_grid: bytes):
        if len(serialized_grid) != CANVAS_SIZE_SERIALIZED:
            raise Exception(
                f"Received invalid canvas array. Should be {CANVAS_SIZE_SERIALIZED} but was {len(serialized_grid)}")
        bitarray_grid = bitarray()
        bitarray_grid.frombytes(serialized_grid)
        with self.canvas_lock:
            for i in range(ROWS):
                for j in range(COLS):
                    self.grid[i][j] = BLACK if bitarray_grid[j * COLS + i] else BG_CANVAS

    def set_pixel(self, col, row, value: int):
        with self.canvas_lock:
            self.grid[col][row] = value  # rgb value

    def set_pixel_by_index(self, index: int):
        if index < 0 or index >= CANVAS_SIZE:
            return
        row = int(index / ROWS)
        col = index % COLS
        self.set_pixel(row, col, BLACK)

    def get_pixel(self, col, row):
        with self.canvas_lock:
            return self.grid[col][row]

    def erase_row_col_area(self, row, col):
        with self.canvas_lock:
            self.grid[col][row] = BG_CANVAS
            for i in range(1, 4):
                offsets = [(col - i, row - i),
                           (col - i, row + i),
                           (col + i, row - i),
                           (col + i, row + i),
                           (col - i, row),
                           (col, row - i),
                           (col + i, row),
                           (col, row + i)]
                for offset in offsets:
                    self.grid[offset[0]][offset[1]] = BG_CANVAS
