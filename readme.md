# Tetris

This repository contains a Tetris game implemented in Python, using the Pygame library.

## How to run the game
1. Install the required dependencies by running `pip install -r requirements.txt`.
2. Run `python main.py` to start the game.

## Controls
- Left arrow: Move the tetromino left.
- Right arrow: Move the tetromino right.
- Up arrow: Rotate the tetromino.
- Down arrow: Move the tetromino down faster.

## Game structure
- `main.py` contains the main game loop and handles user input as well as game logic.
- The `Tetromino` class is responsible for handling individual tetromino shapes, rotations and collisions. Each shape has its own color, shape templates and rotation rules.
- The `Grid` class is responsible for the game grid, adding tetrominos to the grid, clearing lines and detecting if the game is over.
- Colors, dimensions and intervals can be found at the beginning of the code, where they can be easily adjusted as needed.

Happy gaming!