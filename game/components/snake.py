import pygame

from game.config import GRID_HEIGHT, GRID_WIDTH, GRID_SIZE, GREEN, DIRECTIONS


class Snake:
    def __init__(
        self,
        initial_direction=(1, 0),
        initial_position=(GRID_WIDTH // 2, GRID_HEIGHT // 2),
        speed=15,
    ) -> None:
        """
        Initialize the Snake object.

        Args:
            initial_direction (tuple): Initial movement direction (default is right).
            initial_position (tuple): Initial position on the grid (default is the center).
            speed (int): Movement speed (default is 15).
        """
        self.direction = initial_direction
        self.grid = [initial_position]
        self.speed = speed
        self.direction_mapping = {
            "left": (-1, 0),
            "right": (1, 0),
            "up": (0, -1),
            "down": (0, 1),
        }

    def translate_direction(self):
        """
        Translate the current direction into a string.

        Returns:
            str: String representation of the current direction.
        """
        direction_mapping = {v: k for k, v in self.direction_mapping.items()}
        return direction_mapping.get(self.direction, "")

    def rotate(self, direction):
        """
        Rotate the snake's direction based on the input direction.

        Args:
            direction (str): New direction to rotate towards ('left' or 'right').
        """
        current_dir = self.translate_direction()
        if current_dir in DIRECTIONS:
            new_dir = DIRECTIONS.index(current_dir)
        else:
            new_dir = 0
        if direction == "left":
            new_dir = (new_dir - 1) % len(DIRECTIONS)
        elif direction == "right":
            new_dir = (new_dir + 1) % len(DIRECTIONS)

        new_direction = DIRECTIONS[new_dir]
        self.direction = self.direction_mapping.get(new_direction, self.direction)

    def check_collision(self, food):
        """
        Check for collisions with the food.

        Args:
            food (Food): Food object to check for collision with.

        Returns:
            bool: True if collision with food occurred, False otherwise.
        """
        if self.grid[0] == food.position:
            food.reposition()
        else:
            self.grid.pop()

    def move(self):
        """
        Move the snake.

        Returns:
            bool: True if the snake collided with a wall or itself, False otherwise.
        """
        new_head = (
            self.grid[0][0] + self.direction[0],
            self.grid[0][1] + self.direction[1],
        )
        self.grid.insert(0, new_head)

        # Check if the snake hits the wall or itself
        if self.grid[0][0] < 0:
            self.grid[0] = (GRID_WIDTH - 1, self.grid[0][1])
        elif self.grid[0][0] >= GRID_WIDTH:
            self.grid[0] = (0, self.grid[0][1])
        elif self.grid[0][1] < 0:
            self.grid[0] = (self.grid[0][0], GRID_HEIGHT - 1)
        elif self.grid[0][1] >= GRID_HEIGHT:
            self.grid[0] = (self.grid[0][0], 0)

        return self.grid[0] in self.grid[1:]

    def draw(self, screen):
        """
        Draw the snake on the screen.

        Args:
            screen (pygame.Surface): The Pygame screen surface to draw on.
        """
        for segment in self.grid:
            pygame.draw.rect(
                screen,
                GREEN,
                (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE),
            )
