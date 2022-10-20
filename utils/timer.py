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
    elapsed_round_ms: int
    round_start_unix: int
    round_end_unix: int
    round_end_lock: threading.Lock

    # chat
    chat_timer_counter: int

    def __init__(self):
        self.clock = pg.time.Clock()
        self.round_end_lock = threading.Lock()
        self.round_start_lock = threading.Lock()

        self.clear_round()

    def get_round_start(self):
        return self.round_start_unix

    def set_round_start(self, unix_time):
        self.round_start_unix = unix_time

    def get_round_end(self):
        with self.round_end_lock:
            return self.round_end_unix

    def set_round_end(self, end_s):
        if end_s <= 0:
            self.clear_round()
            return

        time_now = int(time.time())
        start_s = end_s - ROUND_DUR_SEC
        time_before_start_s = start_s - time_now

        with self.round_end_lock:
            self.round_end_unix = end_s
            self.round_start_unix = start_s
            self.chat_timer_counter = time_before_start_s

    def clear_round(self):
        with self.round_end_lock:
            self.round_end_unix = 0
            self.round_start_unix = 0
            self.elapsed_round_ms = 0
            self.chat_timer_counter = -1

    def update(self):
        dt = self.clock.tick(FPS)
        self.manage_round_timer()
        self.manage_chat_tick(dt)

    def manage_round_timer(self):
        if 0 < self.get_round_start() <= time.time():
            self.elapsed_round_ms = int((time.time() - self.round_start_unix) * 1000)

    def manage_chat_tick(self, dt):
        self.elapsed_since_last_tick_action_ms += dt
        if self.elapsed_since_last_tick_action_ms > INPUT_TICK_RATE:
            self.elapsed_since_last_tick_action_ms = 0
            self.make_tick = not self.make_tick
