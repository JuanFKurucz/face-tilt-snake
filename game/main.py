import sys

import pygame


from game.config import WIDTH, HEIGHT, WHITE, DIRECTIONS

from game.components.snake import Snake
from game.components.food import Food


# Function to run the game process
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

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

        # ... (update and draw game state) ...
        pygame.display.flip()
        pygame.time.delay(1000 // snake.speed)

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

        # Delay to control the game speed
        pygame.time.delay(1000 // snake.speed)
    pygame.quit()
    sys.exit()
