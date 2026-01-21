import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Check each word in copied set of variable's domain (to avoid modifying set during iteration), 
        # verify that the word's length matches the variable's length
        for variable in self.crossword.variables:
            for word in list(self.domains[variable]):
                if len(word) != variable.length:
                    self.domains[variable].remove(word)
        

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Check if x and y overlap, if they dont, no changes to x's domain will be made, return False
        revision_made = False
        if self.crossword.overlaps[x, y] == None:
            return revision_made
        shared_cell = self.crossword.overlaps[x, y]

        # Nested for loop to compare every word in x's domain with every word in y's domain.
        for word_x in list(self.domains[x]):
            found_acceptable_word = False

            # If there exists a word in y's domain that is compatible with the current word, note it with the boolean
            for word_y in list(self.domains[y]):
                if word_x[shared_cell[0]] == word_y[shared_cell[1]]:
                    found_acceptable_word = True

            # If no compatiable words found in y's domain for the current word, remove it from x's domain, mark that a revision was made
            if found_acceptable_word == False:
                self.domains[x].remove(word_x)
                revision_made = True

        return revision_made

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        from collections import deque

        arc_queue = deque()
        if arcs is None:
            for x in self.crossword.variables:
                for y in self.crossword.variables:
                    if x != y and self.crossword.overlaps[x, y] is not None:
                        arc_queue.append((x, y))
        else:
            arc_queue = deque(arcs)
        
        while len(arc_queue) > 0:
            (x, y) = arc_queue.popleft()
            
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x):
                    if z != y:
                        arc_queue.append((z, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        
        for variable in self.crossword.variables:
            if variable not in assignment or assignment[variable] is None:
                return False

        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Check all words are distinct
        if len(assignment.values()) != len(set(assignment.values())):
            return False
        
        for variable in assignment:
            if len(assignment[variable]) != variable.length:
                return False
            for neighbor in self.crossword.neighbors(variable):
                if neighbor in assignment:
                    shared_cell = self.crossword.overlaps[variable, neighbor]
                    if assignment[variable][shared_cell[0]] != assignment[neighbor][shared_cell[1]]:
                        return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Create dict mapping all possible values of var to the amount of neighboring values 
        # that become incompatible as a result
        num_value_constraints = dict()
        for value in self.domains[var]:
            num_value_constraints[value] = 0

        # Check each value against all values of neighbors to see how many are ruled out
        for value in num_value_constraints:
            for neighbor in self.crossword.neighbors(var):
                # variables already in assignment are not counted toward the total
                if neighbor not in assignment:
                    shared_cell = self.crossword.overlaps[var, neighbor]
                    for neighbor_value in self.domains[neighbor]:
                        if value[shared_cell[0]] != neighbor_value[shared_cell[1]]:
                            num_value_constraints[value] += 1
        # Sort list of values according to to the amount of constraints they create
        list_values = list(self.domains[var])
        list_values.sort(key = lambda value: num_value_constraints[value])

        return list_values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        
        # Create dict mapping variables to the num of values in their domains, if they arent assigned
        num_remaining_values = dict()
        for variable in self.domains:
            if variable not in assignment:
                num_remaining_values[variable] = len(self.domains[variable])

        # Create list from above dict, then sort according to the num of possible values
        list_variables = list(num_remaining_values.keys())
        list_variables.sort(key = lambda value: num_remaining_values[value])

        min_domain_size = num_remaining_values[list_variables[0]]
        
        # Filter out all variables that aren't tied with the variable with least remaining values,
        # then sort again according to the number of neighbors for all tied variables
        tied_variables = [var for var in list_variables if num_remaining_values[var] == min_domain_size]

        if len(tied_variables) > 1:
            tied_variables.sort(key=lambda var: len(self.crossword.neighbors(var)), reverse=True)

        return tied_variables[0]


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        
        var = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if self.consistent(new_assignment):
                assignment[var] = value
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                assignment.pop(var)
        return None




def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
