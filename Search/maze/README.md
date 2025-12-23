# Maze Solver

## Description

This project implements a maze solver using graph search algorithms. The program reads a maze from a text file, finds a path from the starting point (A) to the goal (B), and visualizes the solution.

## Files

- **maze.py**: Main program that implements the maze solver using depth-first search (DFS) or breadth-first search (BFS)
  - `Node`: Represents a state in the search space
  - `StackFrontier`: Implements a stack (LIFO) for DFS
  - `QueueFrontier`: Implements a queue (FIFO) for BFS
  - `Maze`: Main class that loads the maze, solves it, and generates visualization

- **maze1.txt, maze2.txt, maze3.txt**: Sample maze files
  - `A` represents the starting point
  - `B` represents the goal
  - `#` represents walls
  - Spaces represent open paths

- **requirements.txt**: Python dependencies (Pillow for image generation)

## Algorithm

The solver currently uses **Depth-First Search (DFS)** via `StackFrontier`. The algorithm:
- Explores the maze by going deep into paths before backtracking
- Uses graph search (tracks explored states to avoid cycles)
- May not find the shortest path

To use **Breadth-First Search (BFS)** instead (which finds the shortest path), change line 127 in `maze.py`:
```
# Change from:
frontier = StackFrontier()

# To:
frontier = QueueFrontier()
```

## How to Run

1. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

2. **Run the solver**:
   ```
   python maze.py maze1.txt
   ```
   Replace `maze1.txt` with `maze2.txt` or `maze3.txt` to solve different mazes.

3. **Output**:
   - Prints the maze with the solution path marked with `*`
   - Displays the number of states explored to show efficiency/inefficiency of different algorithms
   - Generates `maze.png` showing:
     - Red: Starting point (A)
     - Green: Goal (B)
     - Yellow: Solution path
     - Red/Pink: Explored cells (if enabled)



