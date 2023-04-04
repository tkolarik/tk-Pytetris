import random
import pygame 
SCALE = 30
WINDOW_WIDTH = 10*SCALE
WINDOW_HEIGHT = 24*SCALE
FPS = 60
GRID_SIZE = 1*SCALE

class Tetromino:
    SHAPES = [
        [['.....',
          '.OOO.',
          '..O..',
          '.....'],
         ['..O..',
          '..OO.',
          '..O..',
          '.....'],
         ['..O..',
          '.OOO.',
          '.....',
          '.....',
          ],
         ['..O..',
          '.OO..',
          '..O..',
          '.....',
          ]],
        [['.....',
           '.OOO.',
           '.O...',
           '.....'],
           ['.OO..',
            '..O..',
            '..O..',
            '.....'],
            ['.....',
            '...O.',
            '.OOO.',
            '.....',],
            ['.O...',
             '.O...',
             '.OO..',
             '.....',]],
        [['.....',
           '.O...',
           '.OOO.',
           '.....'],
           ['.OO..',
            '.O...',
            '.O...',
            '.....'],
            ['.....',
            '.OOO.',
            '...O.',
            '.....',],
            ['..O..',
             '..O..',
             '.OO..',
             '.....',]],
        [['.....',
           '.OO..',
           '..OO.',
           '.....'],
           ['..O..',
            '.OO..',
            '.O...',
            '.....'],
            ['.....',
             '.OO..',
             '..OO.',
             '.....'],
           ['..O..',
            '.OO..',
            '.O...',
            '.....']],
        [['.....',
           '..OO.',
           '.OO..',
           '.....'],
           ['..O..',
            '..OO.',
            '...O.',
            '.....'],
            ['.....',
           '..OO.',
           '.OO..',
           '.....'],
           ['..O..',
            '..OO.',
            '...O.',
            '.....']],   
        [['..O..',
           '..O..',
           '..O..',
           '..O..'],
           ['.....',
            '.....',
            'OOOO.',
            '.....'],
            ['..O..',
           '..O..',
           '..O..',
           '..O..'],
           ['.....',
            '.....',
            'OOOO.',
            '.....']],
        [['......',
           '..OO.',
           '..OO.',
           '.....'],
           ['......',
           '..OO.',
           '..OO.',
           '.....'],
           ['......',
           '..OO.',
           '..OO.',
           '.....'],
           ['......',
           '..OO.',
           '..OO.',
           '.....'],]] 
    COLORS = [
        (255, 165, 0),  # Orange
        (255, 255, 0),  # Yellow
        (0, 255, 0),  # Green
        (0, 0, 255),  # Blue
        (128, 0, 128),  # Purple
        (255, 0, 0), # Red
        (0, 255, 255), # Cyan
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, 6)
        self.rotation = 0
        if self.type != 5:  # If the tetromino is not the I shape
            self.y -= GRID_SIZE

    def rotate(self, grid):
        old_rotation = self.rotation
        self.rotation = (self.rotation + 1) % len(self.get_shape())

        jlstz_kicks = [
            [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
            [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
        ]

        i_kicks = [
            [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
            [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
        ]

        if self.type == 6:  # O shape, no rotation needed
            self.rotation = old_rotation
            return

        if self.type == 5:  # I shape
            kicks = i_kicks
        else:  # J, L, S, T, and Z shapes
            kicks = jlstz_kicks

        for dx, dy in kicks[self.rotation % 2]:
            if self.move(grid, dx * GRID_SIZE, dy * GRID_SIZE):
                break
        else:
            self.rotation = old_rotation



    def move(self, grid, dx, dy):
        self.x += dx
        self.y += dy

        if self.collides_with_grid(grid):
            self.x -= dx
            self.y -= dy
            return False

        return True

    def get_shape(self):
        return self.SHAPES[self.type][self.rotation]

    def draw(self, surface, grid):
        for y, row in enumerate(self.get_shape()):
            for x, cell in enumerate(row):
                if cell == 'O' and grid.in_bounds((self.x // GRID_SIZE) + x, (self.y // GRID_SIZE) + y):
                    color = self.COLORS[self.type]
                    pygame.draw.rect(surface, color, (self.x + x * GRID_SIZE + 1, self.y + y * GRID_SIZE + 1, GRID_SIZE - 2, GRID_SIZE - 2), width=0)
                    border_color = tuple(max(c - 50, 0) for c in color)
                    pygame.draw.rect(surface, border_color, (self.x + x * GRID_SIZE, self.y + y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 2)



    def collides_with_grid(self, grid):
        for y, row in enumerate(self.get_shape()):
            for x, cell in enumerate(row):
                if cell == 'O':
                    grid_x = (self.x // GRID_SIZE) + x
                    grid_y = (self.y // GRID_SIZE) + y
                    if not grid.in_bounds(grid_x, grid_y) or not grid.is_empty(grid_x, grid_y):
                        return True
        return False
    
    def move_down(self, grid):
        moved_down = self.move(grid, 0, GRID_SIZE)
        if not moved_down:
            grid.add_tetromino(self)
            grid.clear_lines()

            if grid.game_over():
                return False
            else:
                self.__init__(WINDOW_WIDTH // 2 - GRID_SIZE, 0)
        return True

    def get_positions(self):
        positions = []
        shape = self.SHAPES[self.type][self.rotation]

        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell == "O":
                    positions.append((x + self.x, y + self.y))

        return positions
