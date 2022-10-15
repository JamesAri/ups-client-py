import pygame as pg
from settings import INPUT_TICK_RATE


class Timer:
    clock: pg.time.Clock
    elapsed_since_start: int = 0
    elapsed_since_last_tick_action: int = 0
    make_tick: bool = False

    def __init__(self):
        self.clock = pg.time.Clock()

    def add(self, dt):
        self.elapsed_since_start += dt
        self.elapsed_since_last_tick_action += dt
        if self.elapsed_since_last_tick_action > INPUT_TICK_RATE:
            self.elapsed_since_last_tick_action = 0
            self.make_tick = not self.make_tick
