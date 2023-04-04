import pygame
WHITE = (255, 255, 255)
SCALE = 30
WINDOW_WIDTH = 10*SCALE
WINDOW_HEIGHT = 24*SCALE
FPS = 60
GRID_SIZE = 1*SCALE

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[('.', WHITE) for _ in range(width)] for _ in range(height)]
 
    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def is_empty(self, x, y):
        return self.in_bounds(x, y) and self.grid[y][x][0] == '.'

    def add_tetromino(self, tetromino):
        for y, row in enumerate(tetromino.get_shape()):
            for x, cell in enumerate(row):
                if cell == 'O':
                    grid_x = (tetromino.x // GRID_SIZE) + x
                    grid_y = (tetromino.y // GRID_SIZE) + y
                    if self.in_bounds(grid_x, grid_y):
                        self.grid[grid_y][grid_x] = ('O', tetromino.COLORS[tetromino.type])

    def clear_lines(self):
        self.grid = [row for row in self.grid if not all(cell[0] == 'O' for cell in row)]

        # Add the appropriate number of new lines at the top
        num_lines_cleared = self.height - len(self.grid)
        new_lines = [[('.', WHITE) for _ in range(self.width)] for _ in range(num_lines_cleared)]
        self.grid = new_lines + self.grid

    def draw(self, surface):
        for y, row in enumerate(self.grid):  # Start drawing from the first row
            for x, cell in enumerate(row):
                if cell[0] == 'O':
                    color = cell[1]
                    pygame.draw.rect(surface, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), width=0)
                    border_color = tuple(max(c - 50, 0) for c in color)
                    pygame.draw.rect(surface, border_color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 2)



    def game_over(self):
        for row in range(1):
            for x, cell in enumerate(self.grid[row]):
                if cell[0] == 'O':
                    return True