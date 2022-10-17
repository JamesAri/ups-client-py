import math
import time as time
from settings import *
from client import Client


def get_delta(client: Client):
    time_now = int(time.time())  # unix time
    round_start = client.timer.get_round_start()
    round_end = client.timer.get_round_end()

    start_timer: bool = client.game_in_progress.is_set() and round_end and round_start and round_start <= time_now

    if not start_timer:
        client.can_play.clear()
        return 0
    if time_now >= round_end:
        client.can_play.clear()
        return 1

    if not client.can_play.is_set():
        client.can_play.set()

    # potential_delta = (ROUND_DUR_SEC - round_end - time_now) / ROUND_DUR_SEC
    return client.timer.elapsed_round_ms / ROUND_DUR_MS


def draw_timer(win, client):
    delta = get_delta(client)
    pg.draw.rect(win, BG_TIMER, TIMER_RECT, border_radius=5)
    pg.draw.rect(win, YELLOW, TIMER_RECT, width=2, border_radius=5)
    pg.draw.rect(win, YELLOW,
                 (
                     TIMER_RECT.x,
                     TIMER_RECT.y,
                     TIMER_RECT.w - math.floor(TIMER_RECT.w * delta),
                     TIMER_RECT.h,
                 ),
                 border_radius=5)
