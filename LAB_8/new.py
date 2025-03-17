import pygame
import random
import math

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
SNAKE_PATTERN = (50, 205, 50)  # Lime Green
LADDER_COLOR = (165, 42, 42)  # Brown
LADDER_RUNG = (205, 133, 63)  # Peru (lighter brown)
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

# Dice roll display variables
current_roll = None
show_roll = False
roll_display_time = 0
roll_display_duration = 1500  # 1.5 seconds

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


def draw_snake(start_x, start_y, end_x, end_y):
    # Calculate the distance and angle between start and end
    dx = end_x - start_x
    dy = end_y - start_y
    distance = math.sqrt(dx * dx + dy * dy)
    angle = math.atan2(dy, dx)

    # Number of segments in the snake
    num_segments = int(distance / 15)

    # Draw the snake body (curved path)
    points = []
    amplitude = 10  # How wavy the snake is
    for i in range(num_segments + 1):
        t = i / num_segments
        x = start_x + dx * t
        y = start_y + dy * t

        # Add a sine wave to create the curved snake body
        offset = amplitude * math.sin(t * 8)
        x += offset * math.cos(angle + math.pi / 2)
        y += offset * math.sin(angle + math.pi / 2)

        points.append((x, y))

    # Draw the snake body
    if len(points) > 1:
        pygame.draw.lines(screen, SNAKE_COLOR, False, points, 8)

        # Draw snake pattern (scales)
        for i in range(0, len(points) - 1, 2):
            if i + 1 < len(points):
                pygame.draw.circle(screen, SNAKE_PATTERN, (int(points[i][0]), int(points[i][1])), 4)

    # Draw snake head
    pygame.draw.circle(screen, SNAKE_COLOR, (int(start_x), int(start_y)), 10)

    # Draw snake eyes
    eye_offset_x = 3 * math.cos(angle)
    eye_offset_y = 3 * math.sin(angle)
    pygame.draw.circle(screen, (255, 255, 255), (int(start_x + eye_offset_x + 3 * math.cos(angle + math.pi / 4)),
                                                 int(start_y + eye_offset_y + 3 * math.sin(angle + math.pi / 4))), 2)
    pygame.draw.circle(screen, (255, 255, 255), (int(start_x + eye_offset_x + 3 * math.cos(angle - math.pi / 4)),
                                                 int(start_y + eye_offset_y + 3 * math.sin(angle - math.pi / 4))), 2)

    # Draw snake tail
    tail_x = end_x + 5 * math.cos(angle + math.pi)
    tail_y = end_y + 5 * math.sin(angle + math.pi)
    pygame.draw.circle(screen, SNAKE_COLOR, (int(end_x), int(end_y)), 5)
    pygame.draw.circle(screen, SNAKE_PATTERN, (int(tail_x), int(tail_y)), 3)


def draw_ladder(start_x, start_y, end_x, end_y):
    # Calculate the distance and angle between start and end
    dx = end_x - start_x
    dy = end_y - start_y
    distance = math.sqrt(dx * dx + dy * dy)
    angle = math.atan2(dy, dx)

    # Draw the ladder sides
    side_offset = 5  # Half-width of the ladder

    # Left side of ladder
    left_start_x = start_x + side_offset * math.cos(angle + math.pi / 2)
    left_start_y = start_y + side_offset * math.sin(angle + math.pi / 2)
    left_end_x = end_x + side_offset * math.cos(angle + math.pi / 2)
    left_end_y = end_y + side_offset * math.sin(angle + math.pi / 2)

    # Right side of ladder
    right_start_x = start_x + side_offset * math.cos(angle - math.pi / 2)
    right_start_y = start_y + side_offset * math.sin(angle - math.pi / 2)
    right_end_x = end_x + side_offset * math.cos(angle - math.pi / 2)
    right_end_y = end_y + side_offset * math.sin(angle - math.pi / 2)

    # Draw the sides
    pygame.draw.line(screen, LADDER_COLOR, (left_start_x, left_start_y), (left_end_x, left_end_y), 3)
    pygame.draw.line(screen, LADDER_COLOR, (right_start_x, right_start_y), (right_end_x, right_end_y), 3)

    # Draw the rungs
    num_rungs = int(distance / 20)
    for i in range(num_rungs):
        t = (i + 1) / (num_rungs + 1)
        rung_x = start_x + dx * t
        rung_y = start_y + dy * t

        rung_start_x = rung_x + side_offset * math.cos(angle + math.pi / 2)
        rung_start_y = rung_y + side_offset * math.sin(angle + math.pi / 2)
        rung_end_x = rung_x + side_offset * math.cos(angle - math.pi / 2)
        rung_end_y = rung_y + side_offset * math.sin(angle - math.pi / 2)

        pygame.draw.line(screen, LADDER_RUNG, (rung_start_x, rung_start_y), (rung_end_x, rung_end_y), 2)


def draw_snakes_and_ladders():
    for start, end in snakes.items():
        start_x, start_y = get_coordinates(start)
        end_x, end_y = get_coordinates(end)
        draw_snake(start_x, start_y, end_x, end_y)

    for start, end in ladders.items():
        start_x, start_y = get_coordinates(start)
        end_x, end_y = get_coordinates(end)
        draw_ladder(start_x, start_y, end_x, end_y)


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


def draw_dice(roll_value, is_player):
    # Draw a large dice in the center of the screen
    dice_size = 100
    dice_x = width // 2 - dice_size // 2
    dice_y = height // 2 - dice_size // 2

    # Draw dice background
    pygame.draw.rect(screen, (255, 255, 255), (dice_x, dice_y, dice_size, dice_size))
    pygame.draw.rect(screen, (0, 0, 0), (dice_x, dice_y, dice_size, dice_size), 2)

    # Draw dots based on roll value
    dot_radius = 8
    dot_color = PLAYER_COLOR if is_player else AI_COLOR

    # Positions for dots (normalized coordinates from 0 to 1)
    dot_positions = {
        1: [(0.5, 0.5)],
        2: [(0.25, 0.25), (0.75, 0.75)],
        3: [(0.25, 0.25), (0.5, 0.5), (0.75, 0.75)],
        4: [(0.25, 0.25), (0.25, 0.75), (0.75, 0.25), (0.75, 0.75)],
        5: [(0.25, 0.25), (0.25, 0.75), (0.5, 0.5), (0.75, 0.25), (0.75, 0.75)],
        6: [(0.25, 0.25), (0.25, 0.5), (0.25, 0.75), (0.75, 0.25), (0.75, 0.5), (0.75, 0.75)]
    }

    for pos in dot_positions[roll_value]:
        x = dice_x + int(pos[0] * dice_size)
        y = dice_y + int(pos[1] * dice_size)
        pygame.draw.circle(screen, dot_color, (x, y), dot_radius)

    # Draw text to show whose turn it is
    font = pygame.font.Font(None, 32)
    turn_text = "Player's Roll" if is_player else "AI's Roll"
    text = font.render(turn_text, True, TEXT_COLOR)
    text_rect = text.get_rect(center=(width // 2, dice_y - 20))
    screen.blit(text, text_rect)

    # Draw the roll value
    value_text = f"Rolled: {roll_value}"
    text = font.render(value_text, True, TEXT_COLOR)
    text_rect = text.get_rect(center=(width // 2, dice_y + dice_size + 20))
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

    return roll, min(new_pos, 99)


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
                    button_center[1] - button_radius <= event.pos[1] <= button_center[1] + button_radius and
                    player_turn and not show_roll):
                # Get dice roll but don't move player yet
                roll = random.randint(1, 6)
                current_roll = roll
                show_roll = True
                roll_display_time = pygame.time.get_ticks()

    # Check if it's time to update player position after showing dice
    current_time = pygame.time.get_ticks()
    if show_roll and current_time - roll_display_time > roll_display_duration:
        if player_turn:
            # Calculate new position based on the displayed roll
            new_pos = player_pos + current_roll

            # Check for snakes
            if new_pos in snakes:
                if player_power_ups["shield"] > 0:
                    player_power_ups["shield"] -= 1
                else:
                    new_pos = snakes[new_pos]
            # Check for ladders
            elif new_pos in ladders:
                new_pos = ladders[new_pos]

            # Check for power-ups
            if new_pos in power_up_squares:
                power_up = power_up_squares[new_pos]
                player_power_ups[power_up] += 1

            # Update player position
            player_pos = min(new_pos, 99)
            player_turn = False

            if player_pos == 99:
                print("Player wins!")
                game_over = True

            # Set up AI's turn - automatically roll for AI
            if not game_over:
                roll = random.randint(1, 6)
                current_roll = roll
                show_roll = True
                roll_display_time = pygame.time.get_ticks()
        else:
            # Calculate new position for AI based on the displayed roll
            new_pos = ai_pos + current_roll

            # Check for snakes
            if new_pos in snakes:
                if ai_power_ups["shield"] > 0:
                    ai_power_ups["shield"] -= 1
                else:
                    new_pos = snakes[new_pos]
            # Check for ladders
            elif new_pos in ladders:
                new_pos = ladders[new_pos]

            # Check for power-ups
            if new_pos in power_up_squares:
                power_up = power_up_squares[new_pos]
                ai_power_ups[power_up] += 1

            # Update AI position
            ai_pos = min(new_pos, 99)
            player_turn = True

            if ai_pos == 99:
                print("AI wins!")
                game_over = True

        # Reset dice roll display if game is not over
        if not game_over:
            if player_turn:
                show_roll = False
                current_roll = None
        else:
            # Keep showing the final roll if game is over
            pass

    screen.fill(BACKGROUND)
    draw_board()
    draw_snakes_and_ladders()
    draw_power_ups()

    # Draw the dice if a roll is being shown
    if show_roll:
        draw_dice(current_roll, player_turn)

    draw_players()
    draw_button()
    draw_power_up_info()
    draw_legend()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
