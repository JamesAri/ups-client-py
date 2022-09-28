import math

from utils import *
from layout import *

WIN = pg.display.set_mode((WIDTH, HEIGHT))

# init shared
run = True
timer = Timer()
font = get_font(DEFAULT_FONT_SIZE)

# init canvas
grid = init_grid()

# init chat
active_chat = False
chat = Chat(BUFFER_SIZE)
# print(chat.history_buffer_limit)
text = font.render(chat.current_text, True, GREEN, BLUE)
textRect = text.get_rect(center=((TOOLBAR_SIZE + WIDTH) // 2, HEIGHT // 2))

if __name__ == '__main__':
    while run:
        dt = timer.clock.tick(FPS)
        timer.add(dt)

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
                    chat.add_current_to_history()
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
        draw_chat(WIN, active_chat, font, chat, timer.make_tick and active_chat)
        draw_timer(WIN, timer.elapsed_since_start)
        
        # Redraw
        pg.display.flip()
    pg.quit()
