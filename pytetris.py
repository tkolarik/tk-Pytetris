import pygame
import sys
import random

# Define colors and constants
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
SCALE = 30
WINDOW_WIDTH = 10*SCALE
WINDOW_HEIGHT = 24*SCALE
FPS = 60
GRID_SIZE = 1*SCALE
MOVE_DOWN_EVENT = pygame.USEREVENT + 1
MOVE_DOWN_INTERVAL = 75  # In milliseconds
pygame.font.init() 
game_over_font = pygame.font.Font(None, 36)


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
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
         ['.....',
          '..O..',
          '.OOO.',
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
           ['..OO.',
            '...O.',
            '...O.',
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
           ['..OO.',
            '..O..',
            '..O..',
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
           ['...O.',
            '..OO.',
            '..O..',
            '.....'],
            ['.....',
           '.OO..',
           '..OO.',
           '.....'],
           ['...O.',
            '..OO.',
            '..O..',
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

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.get_shape())

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
                    pygame.draw.rect(surface, self.COLORS[self.type], (self.x + x * GRID_SIZE, self.y + y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

    def collides_with_grid(self, grid):
        for y, row in enumerate(self.get_shape()):
            for x, cell in enumerate(row):
                if cell == 'O':
                    grid_x = (self.x // GRID_SIZE) + x
                    grid_y = (self.y // GRID_SIZE) + y
                    if not grid.is_empty(grid_x, grid_y):
                        return True
        return False


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
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell[0] == 'O':
                    pygame.draw.rect(surface, cell[1], (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

    def game_over(self):
        for row in range(2):
            for x, cell in enumerate(self.grid[row]):
                if cell[0] == 'O':
                    return True



def main():
    running = True
    game_over = False
    grid = Grid(WINDOW_WIDTH // GRID_SIZE, WINDOW_HEIGHT // GRID_SIZE)
    tetromino = Tetromino(WINDOW_WIDTH // 2 - GRID_SIZE, 0)
    pygame.time.set_timer(MOVE_DOWN_EVENT, MOVE_DOWN_INTERVAL)

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == MOVE_DOWN_EVENT and not game_over:
                moved_down = tetromino.move(grid, 0, GRID_SIZE)
                if not moved_down:
                    grid.add_tetromino(tetromino)
                    grid.clear_lines()

                    if grid.game_over():
                        game_over = True
                    else:
                        tetromino = Tetromino(WINDOW_WIDTH // 2 - GRID_SIZE, 0)
                else:
                    pygame.time.set_timer(MOVE_DOWN_EVENT, MOVE_DOWN_INTERVAL)  # Reset the timer
            elif event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_LEFT:
                    tetromino.move(grid, -GRID_SIZE, 0)
                elif event.key == pygame.K_RIGHT:
                    tetromino.move(grid, GRID_SIZE, 0)
                elif event.key == pygame.K_UP:
                    tetromino.rotate()
                elif event.key == pygame.K_DOWN:
                    tetromino.move(grid, 0, GRID_SIZE)

        # Draw the grid and tetromino
        screen.fill(BLACK)
        grid.draw(screen)
        tetromino.draw(screen, grid)

        # Draw game over text if the game is over
        if game_over:
            game_over_text = game_over_font.render('Game Over', True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(game_over_text, text_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()