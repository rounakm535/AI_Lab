import pygame
import random
import tkinter as tk
from tkinter import Button

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 600
CAR_WIDTH, CAR_HEIGHT = 40, 80  # Smaller car size
LANE_WIDTH = WIDTH // 3
BLACK = (0, 0, 0)

# Global variable for mode selection
mode = "human"  # Default mode


def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        return 0


def save_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))


high_score = load_high_score()  # Load high score from file


# Pygame Setup
def game_loop():
    global high_score
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Traffic Racer")

    # Load assets
    road = pygame.image.load("road.png")
    road = pygame.transform.scale(road, (WIDTH, HEIGHT))

    player_car = pygame.image.load("car.png").convert_alpha()
    player_car = pygame.transform.scale(player_car, (CAR_WIDTH, CAR_HEIGHT))

    enemy_cars = [
        pygame.transform.scale(pygame.image.load("enemy1.png").convert_alpha(), (CAR_WIDTH, CAR_HEIGHT)),
        pygame.transform.scale(pygame.image.load("enemy2.png").convert_alpha(), (CAR_WIDTH, CAR_HEIGHT)),
        pygame.transform.scale(pygame.image.load("enemy3.png").convert_alpha(), (CAR_WIDTH, CAR_HEIGHT))
    ]

    # Clock
    clock = pygame.time.Clock()

    # Player position
    lanes = [LANE_WIDTH // 2 - CAR_WIDTH // 2, WIDTH // 2 - CAR_WIDTH // 2, WIDTH - LANE_WIDTH // 2 - CAR_WIDTH // 2]
    player_lane = 1  # Start in the middle lane
    player_x = lanes[player_lane]
    player_y = HEIGHT - CAR_HEIGHT - 20

    # Enemy attributes
    enemies = []
    for _ in range(3):  # Multiple enemy cars
        enemy_x = random.choice(lanes)
        enemy_y = random.randint(-600, -100)
        enemy_type = random.choice(enemy_cars)
        enemies.append([enemy_x, enemy_y, enemy_type])

    enemy_speed = 5
    speed_increment = 0.2  # Faster speed increase
    max_speed = 15  # Limit max speed

    # Score
    score = 0

    running = True
    while running:
        screen.blit(road, (0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and mode == "human":
                if event.key == pygame.K_LEFT and player_lane > 0:
                    player_lane -= 1
                elif event.key == pygame.K_RIGHT and player_lane < 2:
                    player_lane += 1

        # AI Mode Logic - Smart decision-making
        if mode == "ai":
            danger_zones = [HEIGHT] * 3  # Track closest obstacle in each lane
            for enemy in enemies:
                lane_index = lanes.index(enemy[0])
                if enemy[1] > player_y - 150 and enemy[1] < danger_zones[lane_index]:
                    danger_zones[lane_index] = enemy[1]

            safest_lane = max(range(3), key=lambda i: danger_zones[i])

            if safest_lane < player_lane:
                player_lane -= 1
            elif safest_lane > player_lane:
                player_lane += 1

        # Update player position
        player_x = lanes[player_lane]

        # Move enemy cars
        for enemy in enemies:
            enemy[1] += enemy_speed
            if enemy[1] > HEIGHT:
                enemy[1] = random.randint(-600, -100)
                enemy[0] = random.choice(lanes)
                enemy[2] = random.choice(enemy_cars)
                score += 1
                enemy_speed = min(enemy_speed + speed_increment, max_speed)  # Gradually increase speed

        # Collision detection
        for enemy in enemies:
            if player_x == enemy[0] and player_y < enemy[1] + CAR_HEIGHT and player_y + CAR_HEIGHT > enemy[1]:
                print("Game Over! Score:", score)
                high_score = max(high_score, score)
                save_high_score(high_score)  # Save high score to file
                running = False

        # Draw player and enemies
        screen.blit(player_car, (player_x, player_y))
        for enemy in enemies:
            screen.blit(enemy[2], (enemy[0], enemy[1]))

        # Display score and high score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 40))

        # Update display
        pygame.display.update()
        clock.tick(30)

    pygame.quit()


# Function to start the game
def start_game():
    root.destroy()
    game_loop()


# Function to set mode to human
def set_human_mode():
    global mode
    mode = "human"
    start_game()


# Function to set mode to AI
def set_ai_mode():
    global mode
    mode = "ai"
    start_game()


# Home Page GUI using Tkinter
root = tk.Tk()
root.title("Traffic Racer")
root.geometry("400x300")

title_label = tk.Label(root, text="Traffic Racer", font=("Arial", 24))
title_label.pack(pady=20)

human_button = Button(root, text="Play as Human", font=("Arial", 14), command=set_human_mode)
human_button.pack(pady=10)

ai_button = Button(root, text="AI Plays", font=("Arial", 14), command=set_ai_mode)
ai_button.pack(pady=10)

exit_button = Button(root, text="Exit", font=("Arial", 14), command=root.quit)
exit_button.pack(pady=10)

root.mainloop()
