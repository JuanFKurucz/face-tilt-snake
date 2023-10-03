import random

import pygame

from game.config import GRID_HEIGHT, GRID_WIDTH, GRID_SIZE, RED


class Food:
    def __init__(
        self,
        initial_position=(
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1),
        ),
    ) -> None:
        self.position = initial_position

    def reposition(self):
        self.position = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1),
        )

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            RED,
            (
                self.position[0] * GRID_SIZE,
                self.position[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE,
            ),
        )
