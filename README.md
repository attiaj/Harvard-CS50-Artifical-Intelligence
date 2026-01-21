This repo contains project code for the CS50: Artificial Intelligence with Python online course offered by Harvard University. The course is structured in 7 modules: Search, Knowledge, Uncertainty, Optimization, Learning, Neural Networks, and Language.

## **Search**

This module covers search algorithms, such as:
- Depth-First Search
- Breadth-First Search
- Greedy Best-First Search
- A* Search
- Minimax
- Depth-Limited Minimax

### **Project Code**:
- **maze**: Implements DFS and BFS to find the optimal path through a maze, from point A to point B
- **degrees**: Implements BFS to find the shortest path between two actors, in the method of "6 Degrees of Kevin Bacon"
- **tictactoe**: Implements Minimax to create an unbeatable AI in the game TicTacToe

## **Knowledge**

This module covers knowledge representation and logical inference:
- Propositional Logic
- Model Checking
- Theorem Proving
- Inference by Resolution
- First Order Logic

### **Project Code**:
- **knights**: Solves logic puzzles involving knights (who always tell the truth) and knaves (who always lie) using propositional logic and model checking
- **minesweeper**: Implements an AI that uses knowledge representation and inference to play Minesweeper by determining safe cells and mine locations
- **clue**: Uses propositional logic to solve Clue game scenarios by deducing which character, room, and weapon were involved
- **harry**: Additional logic puzzle solving exercises
- **logic**: Core logic library implementing logical sentences, symbols, and inference methods
- **mastermind**: Logic-based solver for the Mastermind code-breaking game
- **puzzle**: Various propositional logic puzzle implementations

## **Uncertainty**

This module covers probabilistic reasoning and inference under uncertainty:
- Bayesian Networks
- Inference by Enumeration
- Approximate Inference (Sampling)
- Markov Chain
- Hidden Markov Model

### **Project Code**:
- **heredity**: Calculates genetic probabilities using Bayesian networks to determine the likelihood of inheriting genes and traits within family relationships
- **pagerank**: Implements PageRank algorithm using both iterative convergence and sampling methods to rank web pages based on link structure
- **bayesnet**: Bayesian network implementation for probabilistic inference using exact and approximate methods
- **chain**: Markov Chain model implementation for representing state transitions and probability distributions
- **hmm**: Hidden Markov Model implementation for sequence analysis and state prediction

## **Optimization**

This module covers optimization techniques and constraint satisfaction:
- Hill Climbing
- Simulated Annealing
- Linear Programming
- Constraint Satisfaction
- Backtracking Search

### **Project Code**:
- **crossword**: Generates crossword puzzles using constraint satisfaction and backtracking search to assign words to grid variables
- **hospitals**: Optimizes hospital placement using hill climbing and simulated annealing to minimize total distance from houses to nearest hospitals
- **production**: Solves production optimization problems using linear programming to maximize profit under resource constraints
- **scheduling**: Implements course scheduling algorithms using constraint satisfaction to assign courses to time slots without conflicts

## **Learning**

This module covers machine learning algorithms:
- Supervised Learning
- Classification
- K-Nearest Neighbors
- Linear Regression
- Logistic Regression
- Cross Validation
- Reinforcement Learning
- Q-Learning
- Unsupervised Learning
- K-Means Clustering

### **Project Code**:
- **nim**: Implements Q-learning reinforcement learning algorithm to train an AI agent to play Nim optimally by learning from experience
- **shopping**: Uses K-Nearest Neighbors (KNN) classification to predict whether online shopping customers will complete a purchase based on their browsing behavior
- **banknotes**: Implements various classification algorithms (KNN, Perceptron, SVM, Naive Bayes) to authenticate banknotes as genuine or counterfeit based on feature measurements
