import random
import pygame
from game.config import GRID_HEIGHT, GRID_WIDTH, GRID_SIZE, RED


class Food:
    """
    Food class represents the food item in the game.

    Attributes:
        position (tuple): The current position of the food item on the grid.
    """

    def __init__(self, initial_position=None):
        """
        Initialize a new Food instance.

        Args:
            initial_position (tuple, optional): The initial position of the food item.
                Defaults to a random position within the grid.
        """
        if initial_position is None:
            initial_position = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1),
            )
        self.position = initial_position

    def reposition(self):
        """
        Reposition the food item to a random location within the grid.
        """
        self.position = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1),
        )

    def draw(self, screen):
        """
        Draw the food item on the game screen.

        Args:
            screen (pygame.Surface): The game screen surface.
        """
        pygame.draw.rect(
            screen,
            RED,
            pygame.Rect(
                self.position[0] * GRID_SIZE,
                self.position[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE,
            ),
        )
