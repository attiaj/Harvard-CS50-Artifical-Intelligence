# Degrees of Separation

## Description

This program finds the shortest path (degrees of separation) between two actors in the IMDB database. It uses breadth-first search (BFS) to find the minimum number of movies connecting two actors through shared co-stars.

## Files

- **degrees.py**: Main program that implements the actor connection finder
  - `load_data()`: Loads actor and movie data from CSV files
  - `shortest_path()`: Uses BFS to find the shortest connection path
  - `neighbors_for_person()`: Finds all actors who have starred with a given person
  - `person_id_for_name()`: Resolves actor names to IDs (handles name ambiguities)

- **util.py**: Contains utility classes for graph search
  - `Node`: Represents a node in the search graph
  - `StackFrontier`: Stack implementation for DFS (can be used but would not find shortest path)
  - `QueueFrontier`: Queue implementation for BFS (used to guarantee shortest path)

- **small/**: Directory containing smaller sample dataset
  - `people.csv`: Actor information
  - `movies.csv`: Movie information
  - `stars.csv`: Actor-movie relationships

- **large/**: Directory containing full IMDB dataset (same structure as small/)

## Algorithm

The program uses **Breadth-First Search (BFS)** to find the shortest path:
- Actors are nodes in the graph
- Edges connect actors who appeared in the same movie
- BFS explores level by level, guaranteeing the shortest path
- Uses graph search (tracks explored states to avoid cycles)

## How to Run


1. **Run the program**:
   ```
   python degrees.py
   ```
   
   Or specify a dataset:
   ```
   python degrees.py small
   python degrees.py large
   ```
   
   Default is `large` if no argument is provided.

3. **Enter actor names when prompted**:
   - The program will ask for two actor names
   - If an actor name has multiple matches, you'll be asked to select the correct one by ID