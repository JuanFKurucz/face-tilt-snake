import sys
import pickle

import pygame
import cv2

from game.components.food import Food
from game.components.snake import Snake
from game.config import HEIGHT, WHITE, WIDTH, BLACK
from game.utils import aspect_scale


# Load or initialize the high score data
try:
    with open("high_scores.pkl", "rb") as f:
        high_scores = pickle.load(f)
except FileNotFoundError:
    high_scores = []


# Function to display the high score table and prompt for player's name
def display_high_scores(screen, score):
    screen.fill(WHITE)
    h1_font = pygame.font.SysFont(None, 36)

    font = pygame.font.SysFont(None, 24)
    y_pos = 100

    required_fields = {"nombre": None, "e-mail": None}

    for key in required_fields:
        screen.fill(WHITE)
        title_text = h1_font.render("High Score", True, BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
        font = pygame.font.SysFont(None, 28)
        name_input_text = font.render(f"Ingresa tu {key}:", True, BLACK)
        screen.blit(
            name_input_text,
            (WIDTH // 2 - name_input_text.get_width() // 2, y_pos + 40),
        )

        pygame.display.flip()

        input_active = True
        player_input = ""
        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        player_input = player_input[:-1]
                    else:
                        player_input += event.unicode
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            name_text = font.render(player_input, True, BLACK)
            screen.fill(WHITE, (WIDTH // 2 - 100, y_pos + 70, 200, 30))
            screen.blit(
                name_text, (WIDTH // 2 - name_text.get_width() // 2, y_pos + 70)
            )
            pygame.display.flip()
        required_fields[key] = player_input

    high_scores.append((required_fields["nombre"], score, required_fields["e-mail"]))

    high_scores.sort(key=lambda x: x[1], reverse=True)
    screen.fill(WHITE)
    title_text = h1_font.render("High Score", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

    for i, (name, high_score, _) in enumerate(high_scores[:10], start=1):
        score_text = font.render(f"{i}. {name}: {high_score}", True, BLACK)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, y_pos))
        y_pos += 30

    # Save the updated high scores
    with open("high_scores.pkl", "wb") as file:
        pickle.dump(high_scores, file)

    pygame.display.flip()
    pygame.time.delay(10000)


def run_game(get_method=None, lock=None, frame_queue=None):
    pygame.init()

    # Initialize the screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")

    snake = Snake()
    food = Food()

    # Game over flag
    game_over = False
    command = "middle"

    # Initialize the font module
    pygame.font.init()
    font = pygame.font.SysFont(None, 30)

    background = aspect_scale(
        pygame.image.load("./game/assets/background/background.png"), WIDTH, HEIGHT
    )
    # Game loop
    frame_start_time = pygame.time.get_ticks()
    while True:
        frame = frame_queue.get()
        cv2.imshow("Deteccion de angulo", frame)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake.rotate("left")
                elif event.key == pygame.K_RIGHT:
                    snake.rotate("right")
        if pygame.time.get_ticks() - frame_start_time >= 1000 / snake.speed:
            frame_start_time = pygame.time.get_ticks()
            if not game_over:
                # Move the snake
                game_over = snake.move()
                snake.check_collision(food)

                screen.blit(background, (0, 0))

                # Draw the score
                score_text = font.render(f"Puntaje: {snake.score}", True, BLACK)
                screen.blit(score_text, (10, 10))

                # Draw the snake
                snake.draw(screen)
                food.draw(screen)

                if get_method() != command:
                    with lock:
                        command = get_method()
                        if command != "middle":
                            snake.rotate(command)
            else:
                display_high_scores(screen, snake.score)
                snake = Snake()
                food = Food()
                game_over = False

            pygame.display.flip()
