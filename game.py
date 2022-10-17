from settings import *
from client import Client

from utils import *
from components import *


def start_game(client: Client):
    run = client.run
    all_chat = client.chat
    canvas = client.canvas

    game_timer = Timer()

    active_chat = False

    while run.is_set():
        dt = game_timer.clock.tick(FPS)
        game_timer.add(dt)

        for event in pg.event.get():
            # LISTEN FOR EXIT
            if event.type == pg.QUIT:
                run.clear()

            # CHAT TRIGGER
            if event.type == pg.MOUSEBUTTONDOWN:
                if CHAT_RECT.collidepoint(event.pos):
                    active_chat = True
                else:
                    active_chat = False

            # CHAT INPUT
            if active_chat and event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    all_chat.use_backspace()
                if event.key == pg.K_RETURN:
                    temp_msg = all_chat.current_text
                    all_chat.add_current_to_history()
                    client.send_guess(temp_msg)
                else:
                    if len(all_chat.current_text) > MAX_MSG_LEN:
                        continue
                    char = event.unicode
                    if char.isalpha() or char == ' ':
                        all_chat.current_text += char
            # DRAWING
            left_pressed, _, right_pressed = pg.mouse.get_pressed()
            if left_pressed:
                try:
                    pos = pg.mouse.get_pos()
                    row, col = get_row_col_pos(pos)
                    canvas.set_pixel(row, col, BLACK)
                    client.send_canvas()
                except IndexError:
                    pass
            elif right_pressed:
                try:
                    pos = pg.mouse.get_pos()
                    row, col = get_row_col_pos(pos)
                    canvas.erase_row_col_area(row, col)
                except IndexError:
                    pass

        # Primary draw functions
        draw_bg(WIN)
        draw_canvas(WIN, canvas)
        draw_chat(WIN, active_chat, FONT, all_chat, game_timer.make_tick and active_chat)
        draw_timer(WIN, game_timer.elapsed_since_start)

        # Redraw
        pg.display.flip()
    pg.quit()
