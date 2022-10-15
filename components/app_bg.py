from settings import *


def draw_bg_img(win):
    for i in range(BG_IMG_X_REPEAT + 1):
        for j in range(BG_IMG_Y_REPEAT + 1):
            win.blit(BG_IMG, (i * BG_IMG.get_width(), j * BG_IMG.get_height()))


def draw_bg(win):
    win.fill(BG_COLOR)
    draw_bg_img(win)
