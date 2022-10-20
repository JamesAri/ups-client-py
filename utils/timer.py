import threading
import time as time

from settings import INPUT_TICK_RATE, ROUND_DUR_SEC, FPS
import pygame as pg


class Timer:
    clock: pg.time.Clock
    can_play = threading.Event()

    # chat input tick-effect
    elapsed_since_last_tick_action_ms: int = 0
    make_tick: bool = False

    # round timer - yellow bar effect
    round_start_unix: int
    round_end_unix: int
    round_end_lock: threading.Lock

    # chat printing
    sec_before_start_timer: int

    def __init__(self):
        self.clock = pg.time.Clock()

        self.can_play = threading.Event()

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
            self.sec_before_start_timer = time_before_start_s

        if time_before_start_s > 0:
            t = threading.Timer(time_before_start_s, self.can_play.set)
            t.daemon = True  # clean exit if necessary
            t.start()
        else:
            self.can_play.set()

    def clear_round(self):
        with self.round_end_lock:
            self.round_end_unix = 0
            self.round_start_unix = 0
            self.sec_before_start_timer = -1

    def decrease_start_timer(self):
        if self.sec_before_start_timer >= 0:
            self.sec_before_start_timer -= 1

    def update(self):
        dt = self.clock.tick(FPS)
        self.manage_chat_tick(dt)

    def manage_chat_tick(self, dt):
        self.elapsed_since_last_tick_action_ms += dt
        if self.elapsed_since_last_tick_action_ms > INPUT_TICK_RATE:
            self.elapsed_since_last_tick_action_ms = 0
            self.make_tick = not self.make_tick
