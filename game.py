import sys
import random

import pygame

from utils import (
    change_direction,
    translate_direction,
    get_face_direction,
    face_direction_lock,
    directions,
)


# Function to run the game process
def run_game():
    pygame.init()
    # Constants
    WIDTH, HEIGHT = 640, 480
    GRID_SIZE = 20
    GRID_WIDTH = WIDTH // GRID_SIZE
    GRID_HEIGHT = HEIGHT // GRID_SIZE
    SNAKE_SPEED = 15  # Increase or decrease to change the game speed

    # Colors
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    # Initialize the screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")

    # Initialize the snake
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    snake_direction = (1, 0)

    # Initialize the food
    food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    # Game over flag
    game_over = False
    command = "middle"

    # Game loop
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != (0, 1):
                    snake_direction = change_direction("top")
                elif event.key == pygame.K_DOWN and snake_direction != (0, -1):
                    snake_direction = change_direction("down")
                elif event.key == pygame.K_LEFT and snake_direction != (1, 0):
                    snake_direction = change_direction("left")
                elif event.key == pygame.K_RIGHT and snake_direction != (-1, 0):
                    snake_direction = change_direction("right")

        # ... (update and draw game state) ...
        pygame.display.flip()
        pygame.time.delay(1000 // SNAKE_SPEED)

        # Move the snake
        new_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])
        snake.insert(0, new_head)

        # Check for collisions
        if snake[0] == food:
            food = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1),
            )
        else:
            snake.pop()

        # Check if the snake hits the wall or itself
        if snake[0][0] < 0:
            snake[0] = (GRID_WIDTH - 1, snake[0][1])
        elif snake[0][0] >= GRID_WIDTH:
            snake[0] = (0, snake[0][1])
        elif snake[0][1] < 0:
            snake[0] = (snake[0][0], GRID_HEIGHT - 1)
        elif snake[0][1] >= GRID_HEIGHT:
            snake[0] = (snake[0][0], 0)

        if snake[0] in snake[1:]:
            game_over = True

        # Clear the screen
        screen.fill(WHITE)

        # Draw the snake
        for segment in snake:
            pygame.draw.rect(
                screen,
                GREEN,
                (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE),
            )

        # Draw the food
        pygame.draw.rect(
            screen,
            RED,
            (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE),
        )

        if get_face_direction() != command:
            with face_direction_lock:
                command = get_face_direction()
                if command != "middle":
                    current_dir = translate_direction(snake_direction)
                    if current_dir in directions:
                        new_dir = directions.index(current_dir)
                    else:
                        new_dir = 0
                    if command == "left":
                        new_dir = (new_dir - 1) % len(directions)
                    elif command == "right":
                        new_dir = (new_dir + 1) % len(directions)
                    snake_direction = change_direction(directions[new_dir])

        pygame.display.flip()

        # Delay to control the game speed
        pygame.time.delay(1000 // SNAKE_SPEED)
    pygame.quit()
    sys.exit()
