import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 1000, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake and Ladder")

# Colors
BACKGROUND = (245, 245, 220)  # Beige
GRID_COLOR = (139, 69, 19)  # Brown
SNAKE_COLOR = (34, 139, 34)  # Forest Green
LADDER_COLOR = (165, 42, 42)  # Brown
TEXT_COLOR = (0, 0, 0)  # Black
BUTTON_COLOR = (70, 130, 180)  # Steel Blue
BUTTON_HIGHLIGHT = (100, 160, 210)  # Lighter Steel Blue
PLAYER_COLOR = (255, 0, 0)  # Red
AI_COLOR = (0, 0, 255)  # Blue

# Game variables
board_size = 10
cell_size = 50
board_width = board_size * cell_size
board_height = board_size * cell_size
board_start_x = 50
board_start_y = (height - board_height) // 2

# Snakes and Ladders (adjusted to start from 0)
snakes = {15: 5, 46: 25, 48: 10, 55: 52, 61: 18, 63: 59, 86: 23, 92: 72, 94: 74, 97: 77}
ladders = {0: 37, 3: 13, 8: 30, 20: 41, 27: 83, 35: 43, 50: 66, 70: 90, 79: 98}

# Power-ups
power_ups = {
    "extra_move": {"color": (255, 165, 0), "count": 3},
    "shield": {"color": (128, 128, 128), "count": 2},
    "teleport": {"color": (138, 43, 226), "count": 1}
}

power_up_squares = {14: "extra_move", 24: "shield", 34: "teleport", 44: "extra_move", 54: "shield", 64: "teleport"}

# Player variables
player_pos = 0
ai_pos = 0
player_power_ups = {"extra_move": 0, "shield": 0, "teleport": 0}
ai_power_ups = {"extra_move": 0, "shield": 0, "teleport": 0}

# Button
button_radius = 60
button_center = (width - 100, height // 2)


def get_coordinates(position):
    row = position // board_size
    col = position % board_size
    if row % 2 == 1:
        col = board_size - 1 - col
    x = board_start_x + col * cell_size + cell_size // 2
    y = board_start_y + (board_size - 1 - row) * cell_size + cell_size // 2
    return x, y


def draw_board():
    for i in range(board_size):
        for j in range(board_size):
            x = board_start_x + j * cell_size
            y = board_start_y + i * cell_size
            rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)

            num = board_size * (board_size - 1 - i) + j
            if (board_size - 1 - i) % 2 == 1:
                num = board_size * (board_size - i) - j - 1
            font = pygame.font.Font(None, 24)
            text = font.render(str(num), True, TEXT_COLOR)
            screen.blit(text, (x + 5, y + 5))


def draw_snakes_and_ladders():
    for start, end in snakes.items():
        start_x, start_y = get_coordinates(start)
        end_x, end_y = get_coordinates(end)
        pygame.draw.line(screen, SNAKE_COLOR, (start_x, start_y), (end_x, end_y), 3)

    for start, end in ladders.items():
        start_x, start_y = get_coordinates(start)
        end_x, end_y = get_coordinates(end)
        pygame.draw.line(screen, LADDER_COLOR, (start_x, start_y), (end_x, end_y), 3)


def draw_players():
    player_x, player_y = get_coordinates(player_pos)
    pygame.draw.circle(screen, PLAYER_COLOR, (player_x, player_y), cell_size // 4)

    ai_x, ai_y = get_coordinates(ai_pos)
    pygame.draw.circle(screen, AI_COLOR, (ai_x, ai_y), cell_size // 4)


def draw_power_ups():
    for pos, power_up in power_up_squares.items():
        x, y = get_coordinates(pos)
        pygame.draw.circle(screen, power_ups[power_up]["color"], (x, y), cell_size // 6)


def draw_power_up_info():
    font = pygame.font.Font(None, 24)
    y_offset = 50
    for power_up, info in power_ups.items():
        text = f"{power_up}: Player {player_power_ups[power_up]}, AI {ai_power_ups[power_up]}"
        text_surface = font.render(text, True, TEXT_COLOR)
        screen.blit(text_surface, (width - 250, y_offset))
        y_offset += 30


def draw_button():
    pygame.draw.circle(screen, BUTTON_HIGHLIGHT, (button_center[0], button_center[1] - 3), button_radius)
    pygame.draw.circle(screen, BUTTON_COLOR, button_center, button_radius)

    font = pygame.font.Font(None, 32)
    text = font.render("Roll", True, TEXT_COLOR)
    text_rect = text.get_rect(center=(button_center[0], button_center[1] - 10))
    screen.blit(text, text_rect)

    text = font.render("Dice", True, TEXT_COLOR)
    text_rect = text.get_rect(center=(button_center[0], button_center[1] + 10))
    screen.blit(text, text_rect)


def draw_legend():
    font = pygame.font.Font(None, 24)

    # Snake legend
    pygame.draw.line(screen, SNAKE_COLOR, (width - 230, height - 120), (width - 180, height - 120), 3)
    text = font.render("Snake", True, TEXT_COLOR)
    screen.blit(text, (width - 170, height - 130))

    # Ladder legend
    pygame.draw.line(screen, LADDER_COLOR, (width - 230, height - 90), (width - 180, height - 90), 3)
    text = font.render("Ladder", True, TEXT_COLOR)
    screen.blit(text, (width - 170, height - 100))

    # Player legend
    pygame.draw.circle(screen, PLAYER_COLOR, (width - 205, height - 60), 10)
    text = font.render("Player", True, TEXT_COLOR)
    screen.blit(text, (width - 170, height - 70))

    # AI legend
    pygame.draw.circle(screen, AI_COLOR, (width - 205, height - 30), 10)
    text = font.render("AI", True, TEXT_COLOR)
    screen.blit(text, (width - 170, height - 40))

    # Power-up legend
    y_offset = height - 150
    for power_up, info in power_ups.items():
        pygame.draw.circle(screen, info["color"], (width - 205, y_offset), 10)
        text = font.render(f"{power_up.capitalize()} Power-up   ", True, TEXT_COLOR)
        screen.blit(text, (width - 185, y_offset - 10))
        y_offset -= 30


def move_player(current_pos, is_player):
    roll = random.randint(1, 6)
    new_pos = current_pos + roll

    if new_pos in snakes:
        if (is_player and player_power_ups["shield"] > 0) or (not is_player and ai_power_ups["shield"] > 0):
            if is_player:
                player_power_ups["shield"] -= 1
            else:
                ai_power_ups["shield"] -= 1
        else:
            new_pos = snakes[new_pos]
    elif new_pos in ladders:
        new_pos = ladders[new_pos]

    if new_pos in power_up_squares:
        power_up = power_up_squares[new_pos]
        if is_player:
            player_power_ups[power_up] += 1
        else:
            ai_power_ups[power_up] += 1

    return min(new_pos, 99)


# Main game loop
clock = pygame.time.Clock()
player_turn = True
game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if (button_center[0] - button_radius <= event.pos[0] <= button_center[0] + button_radius and
                    button_center[1] - button_radius <= event.pos[1] <= button_center[
                        1] + button_radius and player_turn):
                player_pos = move_player(player_pos, True)
                player_turn = False

                if player_pos == 99:
                    print("Player wins!")
                    game_over = True

    if not player_turn and not game_over:
        pygame.time.wait(1000)  # Wait for 1 second before AI moves
        ai_pos = move_player(ai_pos, False)
        player_turn = True

        if ai_pos == 99:
            print("AI wins!")
            game_over = True

    screen.fill(BACKGROUND)
    draw_board()
    draw_snakes_and_ladders()
    draw_power_ups()
    draw_players()
    draw_button()
    draw_power_up_info()
    draw_legend()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()