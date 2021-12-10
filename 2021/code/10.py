import numpy as np
from challenge import Challenge

class ChallengeSolution(Challenge):
    ########################################################################
    #                                Setup                                 #
    ########################################################################

    def __init__(self):
        # Initialise super
        super().__init__()

        # Add complements
        self.complement = {
            '(': ')',
            '[': ']',
            '{': '}',
            '<': '>',
            ')': '(',
            ']': '[',
            '}': '{',
            '>': '<',
        }

        # Add scores illegal
        self.scores_illegal = {
            ')': 3,
            ']': 57,
            '}': 1197,
            '>': 25137,
        }

        # Add scores autocomplete
        self.scores_autocomplete = {
            ')': 1,
            ']': 2,
            '}': 3,
            '>': 4,
        }

    ########################################################################
    #                              Load data                               #
    ########################################################################

    def load(self, path):
        # Load data from path
        with open(path) as infile:
            data = [line.strip() for line in infile.readlines()]

        # Return data
        return data

    ########################################################################
    #                              Exercises                               #
    ########################################################################

    def part_1(self, data):
        # Initialise result
        result = 0

        # Initialise stacks
        self.stack = list()
        # Initialise correctness
        self.errors = list()

        # Loop over all lines
        for index, line in enumerate(data):
            # Create stack
            self.stack.append(list())

            # Check if line is correct
            for character in line:

                # Add opening characters to stack
                if character in '([{<':
                    self.stack[index].append(character)

                # Check if closing character makes sense
                elif character in ')]}>':
                    # Pop last item from the stack
                    complement = self.stack[index].pop(-1)

                    # Check if complement is correct
                    if complement != self.complement[character]:
                        break

                # Check for unknown characters
                else:
                    raise ValueError(f"Unknown character '{character}'")
            else:
                # Check for incomplete
                if self.stack[index]:
                    self.errors.append('incomplete')
                else:
                    self.errors.append(None)
                # Continue
                continue

            # Add score to result
            self.errors.append('corrupted')
            result += self.scores_illegal[character]

        # Return result
        return result

    def part_2(self, data):
        # Initialise result
        result = list()

        # Set autocomplete scores
        score_autocomplete = {
            '(': 1,
            '[': 2,
            '{': 3,
            '<': 4,
        }

        # Loop over all lines and their stack
        for line, stack, error in zip(data, self.stack, self.errors):
            # Check if the stack contains data
            if error == "incomplete":
                # Compute score
                score = 0
                for character in stack[::-1]:
                    score = score * 5 + score_autocomplete[character]

                # Add score
                result.append(score)

        # Compute result
        result = list(sorted(result))
        # Return middle score
        return result[len(result) // 2]
