import threading
import time as time

import pygame as pg
from settings import INPUT_TICK_RATE, ROUND_DUR_SEC, FPS


class Timer:
    clock: pg.time.Clock

    # chat input tick-effect
    elapsed_since_last_tick_action_ms: int = 0
    make_tick: bool = False

    # round timer - yellow bar effect
    elapsed_round_ms: int = 0
    round_start_unix: int = 0  # 0 if not set
    round_end_unix: int = 0  # 0 if not set
    round_end_lock: threading.Lock

    def __init__(self):
        self.clock = pg.time.Clock()
        self.round_end_lock = threading.Lock()
        self.round_start_lock = threading.Lock()

    def get_round_start(self):
        return self.round_start_unix

    def set_round_start(self, unix_time):
        self.round_start_unix = unix_time

    def get_round_end(self):
        with self.round_end_lock:
            return self.round_end_unix

    def set_round_end(self, unix_time):
        with self.round_end_lock:
            self.round_end_unix = unix_time
            start = self.round_end_unix - ROUND_DUR_SEC
            self.set_round_start(start if start > 0 else 0)
            self.elapsed_round_ms = 0

    def update(self):
        dt = self.clock.tick(FPS)
        self.manage_round_timer(dt)
        self.manage_chat_tick(dt)

    def manage_round_timer(self, dt):
        if self.get_round_start() <= time.time():
            self.elapsed_round_ms += dt

    def manage_chat_tick(self, dt):
        self.elapsed_since_last_tick_action_ms += dt
        if self.elapsed_since_last_tick_action_ms > INPUT_TICK_RATE:
            self.elapsed_since_last_tick_action_ms = 0
            self.make_tick = not self.make_tick
