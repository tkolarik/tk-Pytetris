import pygame
import sys
from tetromino import Tetromino, SCALE, WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE
from grid import Grid

class Game:
    FPS = 60
    
    def show_game_over(self):
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.centerx = self.screen.get_rect().centerx
        text_rect.centery = self.screen.get_rect().centery

        self.screen.blit(text, text_rect)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:  # Wait for any key press
                    return
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.grid = Grid(WINDOW_WIDTH // GRID_SIZE, WINDOW_HEIGHT // GRID_SIZE)
        self.tetromino = Tetromino(WINDOW_WIDTH // 2 - GRID_SIZE, 0)
        self.timer_event = pygame.USEREVENT
        pygame.time.set_timer(self.timer_event, 500)
        self.left_counter = 0
        self.right_counter = 0
        self.move_delay = 4

    def run(self):
        while True:
            self.screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.tetromino.rotate(self.grid)
                if event.type == self.timer_event:
                    if not self.tetromino.move_down(self.grid):
                        self.show_game_over()  # Call the function when the game is over
                        pygame.quit()
                        sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:
                if not self.tetromino.move_down(self.grid):
                    break
            if keys[pygame.K_LEFT]:
                self.left_counter += 1
                if self.left_counter % self.move_delay == 0:
                    self.tetromino.move(self.grid, -GRID_SIZE, 0)
            else:
                self.left_counter = 0

            if keys[pygame.K_RIGHT]:
                self.right_counter += 1
                if self.right_counter % self.move_delay == 0:
                    self.tetromino.move(self.grid, GRID_SIZE, 0)
            else:
                self.right_counter = 0

            

            self.grid.draw(self.screen)
            self.tetromino.draw(self.screen, self.grid)

            pygame.display.flip()
            self.clock.tick(self.FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
