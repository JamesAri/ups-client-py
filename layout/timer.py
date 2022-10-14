import math

from utils import *


def draw_timer(win, elapsed):
    pg.draw.rect(win, BG_TIMER, TIMER_RECT, border_radius=5)
    pg.draw.rect(win, YELLOW, TIMER_RECT, width=2, border_radius=5)
    if elapsed <= TIMER_DUR:
        pg.draw.rect(win, YELLOW,
                     (
                         TIMER_RECT.x,
                         TIMER_RECT.y,
                         TIMER_RECT.w - math.floor(TIMER_RECT.w * (elapsed / TIMER_DUR)),
                         TIMER_RECT.h,
                     ),
                     border_radius=5)
