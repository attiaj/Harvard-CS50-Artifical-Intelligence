# Tic-Tac-Toe AI

## Description

An implementation of Tic-Tac-Toe with an AI opponent that uses the Minimax algorithm to play optimally. The game features a graphical interface built with Pygame.

## Files

- **tictactoe.py**: Core game logic and AI implementation
  - `initial_state()`: Returns the starting empty board
  - `player()`: Returns which player's turn it is (X or O)
  - `actions()`: Returns all valid moves for the current board
  - `result()`: Returns a new board after making a move (with validation)
  - `winner()`: Determines the winner (X, O, or None)
  - `terminal()`: Checks if the game is over
  - `utility()`: Returns 1 if X wins, -1 if O wins, 0 for a tie
  - `minimax()`: AI algorithm that finds the optimal move using Minimax
  - `max_value()` and `min_value()`: Helper functions for Minimax recursion

- **runner.py**: Graphical interface using Pygame
  - Handles user interaction and rendering
  - Allows players to choose X or O
  - AI automatically plays the optimal move

- **requirements.txt**: Python dependencies (Pygame for graphics)

- **OpenSans-Regular.ttf**: Font file for the game interface

## Algorithm

The AI uses the **Minimax algorithm** with optimal play:
- Maximizes the score for X (AI tries to win)
- Minimizes the score for O (AI tries to prevent the player from winning)
- Evaluates all possible game states to find the best move
- Guarantees either a win or a tie (never loses)

## How to Run

1. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```


2. **Run the game**:
   ```
   python runner.py
   ```

3. **Play the game**:
   - Choose to play as X or O by clicking the buttons
   - Click on the board to make your move
   - The AI will automatically respond with its move
   - The game ends when someone wins or the board is full


