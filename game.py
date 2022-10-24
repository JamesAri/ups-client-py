from settings import *
from components import *
from client import Client


def start_game(client: Client):
    pg.display.set_caption(f"Draw and Guess! — logged as:   {client.username}")

    run = client.run
    all_chat = client.chat
    canvas = client.canvas
    game_timer = client.timer

    active_chat: bool = False
    player_list_toggle: bool = False
    queue = []

    while run.is_set():
        game_timer.update()

        for event in pg.event.get():
            # LISTEN FOR EXIT
            if event.type == pg.QUIT:
                run.clear()

            if event.type == pg.MOUSEBUTTONDOWN:
                # PLAYER LIST BUTTON
                if PLAYER_LIST_BTN.collidepoint(event.pos):
                    player_list_toggle = not player_list_toggle

            if not client.timer.can_play.is_set():
                active_chat = False
            else:
                # CHAT TRIGGER
                if event.type == pg.MOUSEBUTTONDOWN:
                    if CHAT_RECT.collidepoint(event.pos):
                        active_chat = True
                    else:
                        active_chat = False

                if client.is_drawing.is_set():
                    active_chat = False  # chat opened from previous round

                # CHAT INPUT
                if active_chat:
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_BACKSPACE:
                            all_chat.use_backspace()
                        if event.key == pg.K_RETURN:
                            temp_msg = all_chat.current_text
                            all_chat.add_current_to_history()
                            client.send_guess(temp_msg)
                        else:
                            if len(all_chat.current_text) >= MAX_GUESS_LEN:
                                continue
                            char = event.unicode
                            if char.isalpha() or char == ' ':
                                all_chat.current_text += char
                # DRAWING
                if client.is_drawing.is_set():
                    left_pressed, _, right_pressed = pg.mouse.get_pressed()
                    if left_pressed:
                        try:
                            pos = pg.mouse.get_pos()
                            row, col = get_row_col_pos(pos)
                            pixel = canvas.get_pixel(col, row)
                            if pixel != BLACK:
                                canvas.set_pixel(col, row, BLACK)
                                queue.append((col, row))
                                client.send_canvas_diff(queue)
                        except IndexError:
                            pass
                    elif right_pressed:
                        try:
                            pos = pg.mouse.get_pos()
                            row, col = get_row_col_pos(pos)
                            diffs = canvas.erase_row_col_area(col, row)
                            client.send_canvas_diff(diffs)
                        except IndexError:
                            pass

        # Primary draw functions
        draw_bg(WIN)
        draw_canvas(WIN, canvas)
        draw_chat(WIN, client, active_chat)
        draw_timer(WIN, client)
        draw_toolbox(WIN, client, player_list_toggle)

        # Redraw
        pg.display.flip()  # TODO use update() for better performance
    pg.quit()
