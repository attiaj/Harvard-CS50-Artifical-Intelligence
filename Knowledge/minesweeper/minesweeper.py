from ast import Set
import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        #Only way we can determine if a single sentence contains mines is if the num of mines is equal to the num of cells
        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        #Same logic as above, only one way to determine if a single sentence contains safe cells
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        #Mark the cell as a move and as a safe spot
        self.moves_made.add(cell)
        self.safes.add(cell)

        #Create an initial sentence with all cells surrounding the cell, and the mine count given
        initial_Sentence = Sentence({}, count)
        
        for i in range((cell[0]-1), (cell[0]+2)):
            for j in range((cell[1]-1), (cell[1]+2)):
                if (i >= 0) and (j >= 0) and (i < self.height) and (j < self.width) and ((i, j) != cell):
                    initial_Sentence.cells.add((i, j))

        #Collect cells first to avoid modifying set during iteration
        #Deal with any known mines or safes before adding the initial sentence
        cells_to_check = list(initial_Sentence.cells)
        for cell in cells_to_check:
            if cell in self.mines:
                initial_Sentence.mark_mine(cell)
            elif cell in self.safes:
                initial_Sentence.mark_safe(cell)

        self.knowledge.append(initial_Sentence)

        #Any time a change is made to knowledge base, new inferences are possible, loop until no changes have been made
        while True:
            changes_made = False

            #Collect all mines and safes first (avoid modification during iteration)
            mines_to_mark = set()
            safes_to_mark = set()
            #Check if any mines or safes can be found from the new knowledge base    
            for sentence in self.knowledge:
                mines_to_mark.update(sentence.known_mines())
                safes_to_mark.update(sentence.known_safes())

            #Now mark them
            if mines_to_mark:
                changes_made = True
                for mine in mines_to_mark:
                    self.mark_mine(mine)

            if safes_to_mark:
                changes_made = True
                for safe in safes_to_mark:
                    self.mark_safe(safe)
            
            #Implement subset method inference to find new sentences from existing ones
            for sentence1 in self.knowledge:
                for sentence2 in self.knowledge:
                    if sentence1.cells < sentence2.cells:
                        new_cells = sentence2.cells - sentence1.cells
                        new_count = sentence2.count - sentence1.count
                        new_sentence = Sentence(new_cells, new_count)
                        # Only add if it doesn't already exist and is valid (without this check the same inference can be added indefinitely, infinite loop)
                        if new_sentence not in self.knowledge and len(new_cells) > 0 and new_count >= 0:
                            changes_made = True
                            self.knowledge.append(new_sentence)
            
            # Remove empty sentences at the end (they provide no information)
            self.knowledge = [s for s in self.knowledge if len(s.cells) > 0]
            
            if not changes_made:
                break 
                

        

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        all_random_cells = []
        #Create list of all possible cells that haven't been chosen and also are not currently known as mines
        for i in range(self.height):
            for j in range(self.width):
                if ((i, j) not in self.moves_made) and ((i, j) not in self.mines):
                    all_random_cells.append((i, j))
        #If list is empty, random choice is not possible, otherwise, return a random selection from the list
        if len(all_random_cells) == 0:
            return None
        else:
            return random.choice(all_random_cells)
