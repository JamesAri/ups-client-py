from actions import *

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Draw and Guess!")

run = True
clock = pygame.time.Clock()
grid = init_grid()
font = get_font(25)

chat_rect = pygame.Rect(WIDTH - TOOLBAR_SIZE + PADDING,
                        PADDING,
                        TOOLBAR_SIZE - 2 * PADDING,
                        HEIGHT - 2 * PADDING)

user_text = ''
text = font.render(user_text, True, GREEN, BLUE)
color_active = GRAY
color = color_passive = BLACK
textRect = text.get_rect()

active = False
textRect.center = ((TOOLBAR_SIZE + WIDTH) // 2, HEIGHT // 2)

while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        # LISTEN FOR EXIT
        if event.type == pygame.QUIT:
            run = False

        # CHAT TRIGGER
        if event.type == pygame.MOUSEBUTTONDOWN:
            if chat_rect.collidepoint(event.pos):
                active = True
            else:
                active = False

        # CHAT INPUT
        if active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            if event.key == pygame.K_RETURN:
                # TODO implement history if time
                pass
            else:
                if len(user_text) >= MAX_CHAR:
                    continue
                char = event.unicode
                if char.isalpha() or char == ' ':
                    user_text += char
        # DRAWING
        left_pressed, _, right_pressed = pygame.mouse.get_pressed()
        if left_pressed:
            try:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_pos(pos)
                grid[col][row] = BLACK
            except IndexError:
                pass
        elif right_pressed:
            try:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_pos(pos)
                erase_row_col_area(grid, row, col)
            except IndexError:
                pass
    if active:
        color = color_active
    else:
        color = color_passive

    # Primary draw functions
    draw_bg(WIN)
    draw_canvas(WIN, grid)

    # TODO: implement draw_chat()
    # pygame.draw.rect(WIN, color, input_rect, border_radius=5)

    text_surface = font.render(user_text, True, BLACK)
    pygame.draw.rect(WIN, (80, 80, 80, 127), chat_rect, border_radius=5)
    offset = 3
    input_rec = (chat_rect.x + (TEXT_PADDING - offset),
                 chat_rect.y + chat_rect.height - text_surface.get_height() - TEXT_PADDING,
                 chat_rect.width - 2 * (TEXT_PADDING - offset),
                 text_surface.get_height())
    pygame.draw.rect(WIN, WHITE, input_rec, border_radius=5)
    if active:
        pygame.draw.rect(WIN, RED, input_rec, 1, border_radius=5)
    WIN.blit(text_surface,
             (chat_rect.x + TEXT_PADDING,
              chat_rect.y + chat_rect.height - text_surface.get_height() - TEXT_PADDING))

    # Redraw
    pygame.display.flip()

pygame.quit()

# if __name__ == '__main__':
#     pass
