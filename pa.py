import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600
BG_COLOR = (20, 20, 20)  # Dark theme
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (50, 50, 200)
BUTTON_HOVER_COLOR = (70, 70, 250)
LINE_COLOR = (200, 200, 200)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (84, 84, 84)
LINE_WIDTH = 10
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 20
SPACE = 50

# Fonts
font = pygame.font.Font(None, 80)
button_font = pygame.font.Font(None, 50)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Draw text function
def draw_text(screen, text, x, y, font, color=TEXT_COLOR):
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))

# Button function with rounded corners
def draw_button(screen, text, x, y, width, height, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, width, height)
    if rect.collidepoint(mouse):
        pygame.draw.rect(screen, hover_color, rect, border_radius=15)
        if click[0] == 1 and action:
            action()
    else:
        pygame.draw.rect(screen, color, rect, border_radius=15)

    draw_text(screen, text, x + width // 8, y + height // 5, button_font)

# Draw grid lines with rounded edges
def draw_lines():
    for x in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (x * WIDTH // 3, 0), (x * WIDTH // 3, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, x * HEIGHT // 3), (WIDTH, x * HEIGHT // 3), LINE_WIDTH)

# Draw figures
def draw_figures(board):
    for row in range(3):
        for col in range(3):
            center_x = col * WIDTH // 3 + WIDTH // 6
            center_y = row * HEIGHT // 3 + HEIGHT // 6
            if board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (center_x, center_y), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR, (center_x - SPACE, center_y - SPACE),
                                 (center_x + SPACE, center_y + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (center_x - SPACE, center_y + SPACE),
                                 (center_x + SPACE, center_y - SPACE), CROSS_WIDTH)

# Check winner
def check_winner(board):
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            return board[row][0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    return None

# Human vs AI move
def ai_move(board):
    empty_cells = [(row, col) for row in range(3) for col in range(3) if board[row][col] is None]
    return random.choice(empty_cells) if empty_cells else None

# Restart the game
def restart_game(is_ai):
    play_game(is_ai)

# Main game loop
def play_game(is_ai):
    board = [[None] * 3 for _ in range(3)]
    player = 'O'
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX, mouseY = event.pos
                clicked_row = mouseY // (HEIGHT // 3)
                clicked_col = mouseX // (WIDTH // 3)

                if board[clicked_row][clicked_col] is None:
                    board[clicked_row][clicked_col] = player
                    player = 'X' if player == 'O' else 'O'

                    if is_ai and player == 'X':
                        ai_row, ai_col = ai_move(board)
                        if ai_row is not None:
                            board[ai_row][ai_col] = 'X'
                            player = 'O'

                    winner = check_winner(board)
                    if winner or not any(None in row for row in board):
                        game_over = True

        screen.fill(BG_COLOR)
        draw_lines()
        draw_figures(board)

        if game_over:
            winner = check_winner(board)
            draw_text(screen, f"{winner or 'Draw'} Wins!", WIDTH // 4, HEIGHT // 2 - 40, font)
            draw_button(screen, "Restart", WIDTH // 4, HEIGHT // 2 + 50, WIDTH // 2, 50, BUTTON_COLOR, BUTTON_HOVER_COLOR, lambda: restart_game(is_ai))
            draw_button(screen, "Back to Menu", WIDTH // 4, HEIGHT // 2 + 120, WIDTH // 2, 50, BUTTON_COLOR, BUTTON_HOVER_COLOR, menu)
        
        pygame.display.update()

# Menu screen
def menu():
    while True:
        screen.fill(BG_COLOR)
        draw_text(screen, "Tic Tac Toe", WIDTH // 2 - 150, 50, font)

        draw_button(screen, "Human vs Human", WIDTH // 4, HEIGHT // 3, WIDTH // 2, 50,
                    BUTTON_COLOR, BUTTON_HOVER_COLOR, lambda: play_game(False))
        draw_button(screen, "Human vs Computer", WIDTH // 4, HEIGHT // 2, WIDTH // 2, 50,
                    BUTTON_COLOR, BUTTON_HOVER_COLOR, lambda: play_game(True))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Start the game
if __name__ == "__main__":
    menu()
