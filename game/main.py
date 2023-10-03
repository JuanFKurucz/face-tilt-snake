import sys

import pygame

from game.components.food import Food
from game.components.snake import Snake
from game.config import HEIGHT, WHITE, WIDTH


def run_game(get_method=None, lock=None):
    pygame.init()

    # Initialize the screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")

    snake = Snake()
    food = Food()

    # Game over flag
    game_over = False
    command = "middle"

    # Create a clock object to control the frame rate
    clock = pygame.time.Clock()

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not game_over:
            # Move the snake
            game_over = snake.move()
            snake.check_collision(food)

            # Clear the screen
            screen.fill(WHITE)

            # Draw the snake
            snake.draw(screen)
            food.draw(screen)

            if get_method() != command:
                with lock:
                    command = get_method()
                    if command != "middle":
                        snake.rotate(command)

        pygame.display.flip()

        # Use the clock to control the game speed
        clock.tick(snake.speed)
