import pygame

from game.config import GRID_HEIGHT, GRID_WIDTH, GRID_SIZE, GREEN, DIRECTIONS


class Snake:
    def __init__(
        self,
        initial_direction=(1, 0),
        initial_position=(GRID_WIDTH // 2, GRID_HEIGHT // 2),
        speed=15,
    ) -> None:
        self.direction = initial_direction
        self.grid = [initial_position]
        self.speed = speed

    def translate_direction(self):
        if self.direction == (0, 1):
            return "down"
        elif self.direction == (0, -1):
            return "up"
        elif self.direction == (1, 0):
            return "right"
        elif self.direction == (-1, 0):
            return "left"

    def rotate(self, direction):
        current_dir = self.translate_direction()
        if current_dir in DIRECTIONS:
            new_dir = DIRECTIONS.index(current_dir)
        else:
            new_dir = 0
        if direction == "left":
            new_dir = (new_dir - 1) % len(DIRECTIONS)
        elif direction == "right":
            direction = (new_dir + 1) % len(DIRECTIONS)

        new_direction = DIRECTIONS[new_dir]
        if new_direction == "left":
            self.direction = (-1, 0)
        elif new_direction == "right":
            self.direction = (1, 0)
        elif new_direction == "up":
            self.direction = (0, -1)
        elif new_direction == "down":
            self.direction = (0, 1)

    def check_collision(self, food):
        # Check for collisions
        if self.grid[0] == food:
            food.reposition()
        else:
            self.grid.pop()

    def move(self):
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

        if self.grid[0] in self.grid[1:]:
            return True
        return False

    def draw(self, screen):
        # Draw the snake
        for segment in self.grid:
            pygame.draw.rect(
                screen,
                GREEN,
                (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE),
            )
