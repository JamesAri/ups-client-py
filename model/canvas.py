import threading
from bitarray import bitarray

from settings import ROWS, COLS, BG_CANVAS, CANVAS_SIZE, BLACK, CANVAS_SIZE_SERIALIZED


class Canvas:
    grid: list
    grid_serialized: bitarray
    canvas_lock: threading.Lock

    def __init__(self):
        self.__init_grid()
        self.canvas_lock = threading.Lock()
        self.grid_serialized = bitarray(CANVAS_SIZE)
        self.grid_serialized.setall(0)

    def __init_grid(self):
        self.grid = []
        for i in range(ROWS):
            self.grid.append([])
            for _ in range(COLS):
                self.grid[i].append(BG_CANVAS)
        return self.grid

    def unpack_and_set(self, serialized_grid: bytes):
        if len(serialized_grid) != CANVAS_SIZE_SERIALIZED:
            raise Exception("Received invalid canvas array")
        with self.canvas_lock:
            for i in range(ROWS):
                for j in range(COLS):
                    self.grid_serialized.clear()
                    self.grid_serialized.frombytes(serialized_grid)
                    self.grid[i][j] = BLACK if self.grid_serialized[j * COLS + i] else BG_CANVAS

    def set_pixel(self, row, col, value: int):
        with self.canvas_lock:
            self.grid[col][row] = value  # rgb value
            self.grid_serialized[row * COLS + col] = 1 if value else 0

    def erase_row_col_area(self, row, col):
        with self.canvas_lock:
            self.grid[col][row] = BG_CANVAS
            for i in range(1, 4):
                offset = (col - i, row - i)
                self.grid[offset[0]][offset[1]] = BG_CANVAS
                self.grid_serialized[offset[1] * COLS + offset[0]] = 0
                offset = (col - i, row + i)
                self.grid[offset[0]][offset[1]] = BG_CANVAS
                self.grid_serialized[offset[1] * COLS + offset[0]] = 0
                offset = (col + i, row - i)
                self.grid[offset[0]][offset[1]] = BG_CANVAS
                self.grid_serialized[offset[1] * COLS + offset[0]] = 0
                offset = (col + i, row + i)
                self.grid[offset[0]][offset[1]] = BG_CANVAS
                self.grid_serialized[offset[1] * COLS + offset[0]] = 0
                offset = (col - i, row)
                self.grid[offset[0]][offset[1]] = BG_CANVAS
                self.grid_serialized[offset[1] * COLS + offset[0]] = 0
                offset = (col, row - i)
                self.grid[offset[0]][offset[1]] = BG_CANVAS
                self.grid_serialized[offset[1] * COLS + offset[0]] = 0
                offset = (col + i, row)
                self.grid[offset[0]][offset[1]] = BG_CANVAS
                self.grid_serialized[offset[1] * COLS + offset[0]] = 0
                offset = (col, row + i)
                self.grid[offset[0]][offset[1]] = BG_CANVAS
                self.grid_serialized[offset[1] * COLS + offset[0]] = 0
