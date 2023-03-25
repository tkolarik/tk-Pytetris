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
MOVE_DOWN_INTERVAL = 150  # In milliseconds
FAST_MOVE_INTERVAL = 25 # In milliseconds
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

        if self.type == 0:  # T shape
            kick_data = [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)]
        elif self.type == 1 or self.type == 2:  # L and J shapes
            if self.rotation % 2 == 1:  # Clockwise
                kick_data = [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)]
            else:  # Counterclockwise
                kick_data = [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)]
        elif self.type == 3 or self.type == 4:  # S and Z shapes
            kick_data = [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)]
        elif self.type == 5:  # I shape
            if self.rotation % 2 == 1:  # Clockwise
                kick_data = [(0, 0), (-1, 0), (1, 0), (-2, -1), (2, 2)]
            else:  # Counterclockwise
                kick_data = [(0, 0), (-1, 0), (2, 0), (-1, -1), (2, 2)]
        else:  # O shape, no rotation needed
            self.rotation = old_rotation
            return

        for dx, dy in kick_data:
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



def main():
    running = True
    game_over = False
    grid = Grid(WINDOW_WIDTH // GRID_SIZE, WINDOW_HEIGHT // GRID_SIZE)
    tetromino = Tetromino(WINDOW_WIDTH // 2 - GRID_SIZE, 0)
    pygame.time.set_timer(MOVE_DOWN_EVENT, MOVE_DOWN_INTERVAL)
    fast_move_down = False
    
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == MOVE_DOWN_EVENT and not game_over:
                if fast_move_down:  # If down arrow key is held, use FAST_MOVE_INTERVAL
                    interval = FAST_MOVE_INTERVAL
                else:
                    interval = MOVE_DOWN_INTERVAL
                pygame.time.set_timer(MOVE_DOWN_EVENT, interval)
                if not tetromino.move_down(grid):
                    game_over = True  # Reset the timer
            elif event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_LEFT:
                    tetromino.move(grid, -GRID_SIZE, 0)
                elif event.key == pygame.K_RIGHT:
                    tetromino.move(grid, GRID_SIZE, 0)
                elif event.key == pygame.K_UP:
                    tetromino.rotate(grid)
                elif event.key == pygame.K_DOWN:
                    tetromino.move(grid, 0, GRID_SIZE)
                    fast_move_down = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    fast_move_down = False  # Reset the flag when the down arrow key is released


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
