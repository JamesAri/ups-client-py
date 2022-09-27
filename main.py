import math

from actions import *

WIN = pg.display.set_mode((WIDTH, HEIGHT))

# init shared
run = True
clock = pg.time.Clock()
font = get_font(DEFAULT_FONT_SIZE)
elapsed_since_start = 0
elapsed_since_last_tick_action = 0
make_tick = False

# init canvas
grid = init_grid()

# init chat
active_chat = False
chat = Chat()
text = font.render(chat.current_text, True, GREEN, BLUE)
textRect = text.get_rect(center=((TOOLBAR_SIZE + WIDTH) // 2, HEIGHT // 2))

if __name__ == '__main__':
    while run:
        dt = clock.tick(FPS)
        elapsed_since_start += dt

        for event in pg.event.get():
            # LISTEN FOR EXIT
            if event.type == pg.QUIT:
                run = False

            # CHAT TRIGGER
            if event.type == pg.MOUSEBUTTONDOWN:
                if CHAT_RECT.collidepoint(event.pos):
                    active_chat = True
                else:
                    active_chat = False

            # CHAT INPUT
            if active_chat and event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    chat.use_backspace()
                if event.key == pg.K_RETURN:
                    # TODO implement history if time
                    pass
                else:
                    if len(chat.current_text) >= MAX_CHAR:
                        continue
                    char = event.unicode
                    if char.isalpha() or char == ' ':
                        chat.current_text += char
            # DRAWING
            left_pressed, _, right_pressed = pg.mouse.get_pressed()
            if left_pressed:
                try:
                    pos = pg.mouse.get_pos()
                    row, col = get_row_col_pos(pos)
                    grid[col][row] = BLACK
                except IndexError:
                    pass
            elif right_pressed:
                try:
                    pos = pg.mouse.get_pos()
                    row, col = get_row_col_pos(pos)
                    erase_row_col_area(grid, row, col)
                except IndexError:
                    pass

        # Primary draw functions
        draw_bg(WIN)
        draw_canvas(WIN, grid)

        elapsed_since_last_tick_action += dt
        if elapsed_since_last_tick_action > INPUT_TICK_RATE:
            elapsed_since_last_tick_action = 0
            make_tick = not make_tick

        draw_chat(WIN, active_chat, font, chat, make_tick and active_chat)

        pg.draw.rect(WIN, BG_TIMER, TIMER_RECT, border_radius=5)
        pg.draw.rect(WIN, YELLOW, TIMER_RECT, width=2, border_radius=5)
        pg.draw.rect(WIN, YELLOW,
                     (
                         TIMER_RECT.x,
                         TIMER_RECT.y,
                         TIMER_RECT.w - math.floor(TIMER_RECT.w * (elapsed_since_start / TIMER_DUR)),
                         TIMER_RECT.h,
                     ),
                     border_radius=5)

        # Redraw
        pg.display.flip()
    pg.quit()
