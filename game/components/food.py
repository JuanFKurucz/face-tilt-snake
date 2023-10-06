import os
import random

import pygame

from game.config import GRID_HEIGHT, GRID_SIZE, GRID_WIDTH


def aspect_scale(img, bx, by):
    """Scales 'img' to fit into box bx/by.
    This method will retain the original image's aspect ratio"""
    ix, iy = img.get_size()
    if ix > iy:
        # fit to width
        scale_factor = bx / float(ix)
        sy = scale_factor * iy
        if sy > by:
            scale_factor = by / float(iy)
            sx = scale_factor * ix
            sy = by
        else:
            sx = bx
    else:
        # fit to height
        scale_factor = by / float(iy)
        sx = scale_factor * ix
        if sx > bx:
            scale_factor = bx / float(ix)
            sx = bx
            sy = scale_factor * iy
        else:
            sy = by

    return pygame.transform.scale(img, (sx, sy))


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
        self.width = 5
        self.height = 5

        if initial_position is None:
            initial_position = self.get_random_position()

        self.position = initial_position

        self.image = self.get_random_image()

    def get_random_position(self):
        return (
            random.randint(0, GRID_WIDTH - 1 - self.width),
            random.randint(0, GRID_HEIGHT - 1 - self.height),
        )

    def get_random_image(self):
        path = "./game/assets/food"
        files = os.listdir(path)
        index = random.randrange(0, len(files))
        image = aspect_scale(
            pygame.image.load(path + "/" + files[index]),
            self.width * GRID_SIZE,
            self.height * GRID_SIZE,
        )
        return image

    def reposition(self):
        """
        Reposition the food item to a random location within the grid.
        """
        self.position = self.get_random_position()
        self.image = self.get_random_image()

    def draw(self, screen):
        """
        Draw the food item on the game screen.

        Args:
            screen (pygame.Surface): The game screen surface.
        """
        screen.blit(
            self.image,
            (
                self.position[0] * GRID_SIZE,
                self.position[1] * GRID_SIZE,
            ),
        )
