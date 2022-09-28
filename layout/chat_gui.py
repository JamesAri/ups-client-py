from utils import *


def draw_input_bg(win, active):
    input_border_padding = 2
    pg.draw.rect(win, WHITE, INPUT_REC)
    pg.draw.rect(win, YELLOW if active else BLACK,
                 (
                     INPUT_REC.x - input_border_padding,
                     INPUT_REC.y - input_border_padding,
                     INPUT_REC.w + 2 * input_border_padding,
                     INPUT_REC.h + 2 * input_border_padding,
                 ),
                 width=2, border_radius=2)


def make_input(win, font, chat, make_input_tick):
    text_surface = font.render(chat.current_text, True, BLACK)
    win.blit(text_surface, (CHAT_RECT.x + TEXT_PADDING,
                            CHAT_RECT.y + CHAT_RECT.height - text_surface.get_height() - TEXT_PADDING))
    if make_input_tick:
        do_input_tick(win, text_surface)


def draw_chat_history(win, font, chat: Chat):
    texts = [font.render(text, True, GRAY) for text in chat.history]
    for i, text in enumerate(texts, 1):
        win.blit(text, (INPUT_REC.x, INPUT_REC.y - i * FONT_HEIGHT - HISTORY_CHAT_INPUT_PADDING))


def draw_chat_layout(win, active, font, chat):
    # BG
    win.blit(CHAT_SURF, (CHAT_RECT.x, CHAT_RECT.y))

    # CHAT HISTORY
    draw_chat_history(win, font, chat)

    # BORDER
    pg.draw.rect(win, BLACK, CHAT_RECT, width=1, border_radius=5)
    # INPUT
    draw_input_bg(win, active)


def do_input_tick(win, text_surface):
    pg.draw.line(win, BLACK,
                 (
                     CHAT_RECT.x + TEXT_PADDING + text_surface.get_width() + 1,
                     CHAT_RECT.y + CHAT_RECT.height - text_surface.get_height() - TEXT_PADDING + 3,
                 ),
                 (
                     CHAT_RECT.x + TEXT_PADDING + text_surface.get_width() + 1,
                     CHAT_RECT.y + CHAT_RECT.height - text_surface.get_height() - TEXT_PADDING + text_surface.get_height() - 3
                 ))


def draw_chat(win, active, font, chat: Chat, make_input_tick):
    draw_chat_layout(win, active, font, chat)
    make_input(win, font, chat, make_input_tick)
