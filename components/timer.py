from settings import *
from client import Client

import math
import time as time


def get_delta(client: Client):
    """ returns completion of round timer in percentage """
    time_now: int = int(time.time())
    round_start: int = client.timer.get_round_start()
    round_end: int = client.timer.get_round_end()
    sec_before_start: int = client.timer.sec_before_start_timer

    if sec_before_start >= 0 and client.game_in_progress.is_set():
        print_msg = (round_start - time_now) <= sec_before_start
        if print_msg:
            if sec_before_start:
                msg = f"round starts in {int(sec_before_start)}s"
                client.chat.add_to_history((msg, RED))
            else:
                client.chat.add_to_history(("start", RED))
            client.timer.decrease_start_timer()

    start_timer: bool = \
        client.game_in_progress.is_set() and round_start <= time_now

    if not start_timer:
        # client.can_play.clear()
        return 0
    if time_now >= round_end:
        # client.can_play.clear()
        return 1

    # if not client.can_play.is_set():
    #     client.can_play.set()

    return int((time.time() - round_start) * 1000) / ROUND_DUR_MS


def draw_timer(win, client):
    delta = get_delta(client)
    pg.draw.rect(win, BG_TIMER, TIMER_RECT, border_radius=5)
    pg.draw.rect(win, YELLOW, TIMER_RECT, width=2, border_radius=5)
    pg.draw.rect(win, YELLOW,
                 (
                     TIMER_RECT.x,
                     TIMER_RECT.y,
                     TIMER_RECT.w - math.floor(TIMER_RECT.w * (delta if delta < 1 else 1)),
                     TIMER_RECT.h,
                 ),
                 border_radius=5)
