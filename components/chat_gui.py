from settings import *
from model import Chat
from client.client import Client

__input_border_width = 1
__input_tick_padding_x = 1
__input_tick_padding_y = 3


def draw_input_area(win, active):
    pg.draw.rect(win, WHITE, INPUT_REC)
    pg.draw.rect(win, YELLOW if active else BLACK,
                 (
                     INPUT_REC.x - __input_border_width,
                     INPUT_REC.y - __input_border_width,
                     INPUT_REC.w + 2 * __input_border_width,
                     INPUT_REC.h + 2 * __input_border_width,
                 ),
                 width=__input_border_width, border_radius=2)


def make_input(win, chat, make_input_tick):
    text_surface = FONT.render(chat.current_text, True, BLACK)
    win.blit(text_surface, (INPUT_REC.x + TEXT_PADDING, INPUT_REC.y))
    if make_input_tick:
        do_input_tick(win, text_surface)


def do_input_tick(win, text_surface):
    pg.draw.line(win, BLACK,
                 (
                     INPUT_REC.x + text_surface.get_width() + TEXT_PADDING + __input_tick_padding_x,
                     INPUT_REC.y + __input_tick_padding_y,
                 ),
                 (
                     INPUT_REC.x + text_surface.get_width() + TEXT_PADDING + __input_tick_padding_x,
                     INPUT_REC.y + INPUT_REC.h - __input_tick_padding_y,
                 ))


def draw_chat_history(win, chat: Chat):
    # texts = [FONT.render(text, True, color) for (text, color) in chat.history]
    for i, (text, color) in enumerate(chat.history, 1):
        text_surface = FONT.render(text, True, color)
        win.blit(text_surface, (INPUT_REC.x, INPUT_REC.y - i * FONT_HEIGHT - HISTORY_CHAT_INPUT_PADDING))


def draw_chat_layout(win, active, chat):
    # BG
    win.blit(CHAT_SURF, (CHAT_RECT.x, CHAT_RECT.y))

    # CHAT HISTORY
    draw_chat_history(win, chat)

    # BORDER
    pg.draw.rect(win, BLACK, CHAT_RECT, width=CHAT_BORDER_WIDTH, border_radius=CHAT_BORDER_RADIUS)

    # INPUT
    draw_input_area(win, active)


def draw_chat(win, client: Client, active_chat):
    draw_chat_layout(win, active_chat, client.chat)
    make_input(win, client.chat, make_input_tick=client.timer.make_tick and active_chat)
