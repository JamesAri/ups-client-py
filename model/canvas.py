import threading

from settings import ROWS, COLS, BG_CANVAS


class Canvas:
    grid: list
    grid_serialized: bytearray
    canvas_lock: threading.Lock

    def __init__(self):
        self.__init_grid()
        self.canvas_lock = threading.Lock()
        self.grid_serialized = bytearray(ROWS * COLS)

    def __init_grid(self):
        self.grid = []
        for i in range(ROWS):
            self.grid.append([])
            for _ in range(COLS):
                self.grid[i].append(BG_CANVAS)
        return self.grid

    def unpack_and_set(self, byte_arr: bytearray):
        if len(byte_arr) != len(self.grid):
            raise Exception("Received invalid canvas array")
        with self.canvas_lock:
            for i in ROWS:
                for j in COLS:
                    self.grid_serialized = byte_arr
                    self.grid[i][j] = byte_arr[i * COLS + j]

    def set_pixel(self, row, col, value: int):
        with self.canvas_lock:
            self.grid[row][col] = value  # rgb value
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
