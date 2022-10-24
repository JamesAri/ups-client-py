from settings import *
from client import Client

__pl_padding = 3
__circle_text_spacing = 5
__x_text = PLAYER_LIST_RECT.x + TEXT_PADDING
__x_circle = __x_text + STATUS_CIRCLE_RADIUS


def draw_player_list(win: pg.Surface, client: Client):
    PLAYER_LIST_RECT.h = client.get_num_of_players() * FONT_HEIGHT + __pl_padding
    pg.draw.rect(win, WHITE, PLAYER_LIST_RECT,
                 border_radius=CHAT_BORDER_RADIUS)
    pg.draw.rect(win, BLACK, PLAYER_LIST_RECT,
                 width=1, border_radius=CHAT_BORDER_RADIUS)
    with client.players_lock:
        for i, (username, status) in enumerate(client.players.items()):
            y_text = PLAYER_LIST_RECT.y + i * FONT_HEIGHT
            y_circle = y_text + STATUS_CIRCLE_DIAMETER
            pg.draw.circle(win, GREEN if status else RED, (__x_circle, y_circle), STATUS_CIRCLE_RADIUS)
            text_surface = FONT.render(username, True, BLACK)
            win.blit(text_surface, (__x_text + STATUS_CIRCLE_DIAMETER + __circle_text_spacing, y_text))


def draw_player_list_btn(win: pg.Surface):
    pg.draw.rect(win, WHITE, PLAYER_LIST_BTN,
                 border_radius=BUTTON_RADIUS)
    pg.draw.rect(win, BLACK, PLAYER_LIST_BTN,
                 width=1, border_radius=BUTTON_RADIUS)
    win.blit(PLAYER_LIST_IMG, PLAYER_LIST_IMG_POS)


def draw_toolbox(win: pg.Surface, client: Client, on: bool):
    draw_player_list_btn(win)
    if on:
        draw_player_list(win, client)
