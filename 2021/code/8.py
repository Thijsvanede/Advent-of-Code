import itertools
import numpy as np
from challenge import Challenge

class ChallengeSolution(Challenge):

    def __init__(self):
        # Initialise super
        super().__init__()

        # Define digit masks
        self.digits = np.asarray([
            [True , True , True , False, True , True , True ], # 0
            [False, False, True , False, False, True , False], # 1
            [True , False, True , True , True , False, True ], # 2
            [True , False, True , True , False, True , True ], # 3
            [False, True , True , True , False, True , False], # 4
            [True , True , False, True , False, True , True ], # 5
            [True , True , False, True , True , True , True ], # 6
            [True , False, True , False, False, True , False], # 7
            [True , True , True , True , True , True , True ], # 8
            [True , True , True , True , False, True , True ], # 9
        ])

        # Length dict
        # 1 = len(2), 4 = len(4), 7 = len(3), 8 = len(7)
        self.fixed_lengths = {2, 3, 4, 7}

    ########################################################################
    #                              Load data                               #
    ########################################################################

    def load(self, path):
        # Load data from path
        with open(path) as infile:
            data = infile.read().strip().split('\n')

        # Parse data
        for i, item in enumerate(data):
            crossed, target = item.split(' | ')
            data[i] = (
                [set(x) for x in crossed.split()],
                [set(x) for x in target .split()],
            )

        # Return data
        return data

    ########################################################################
    #                              Exercises                               #
    ########################################################################

    def part_1(self, data):
        # Initialise result
        result = 0

        # Loop over data
        for crossed, target in data:
            result += sum([len(x) in self.fixed_lengths for x in target])

        # Return result
        return result

    def part_2(self, data):
        # Initialise result
        result = 0

        # Loop over all data
        for crossed, target in data:
            # Sort crossed by length
            crossed = list(sorted(crossed, key=lambda x: len(x)))

            # Define each number in crossed
            one   = crossed[0]
            four  = crossed[2]
            seven = crossed[1]
            eight = crossed[9]
            three = [x for x in crossed[3:6] if len(x & one  ) == 2][0]
            six   = [x for x in crossed[6:9] if len(x & one  ) == 1][0]
            zero  = [x for x in crossed[6:9] if len(x | three) == 7 and x != six  ][0]
            nine  = [x for x in crossed[6:9] if len(x | three) != 7][0]
            two   = [x for x in crossed[3:6] if len(x | nine ) == 7 and x != three][0]
            five  = [x for x in crossed[3:6] if len(x | nine ) == 6 and x != three][0]

            # Define numbers
            crossed = [zero,one,two,three,four,five,six,seven,eight,nine]

            # Check where target equals crossed
            for i, x in enumerate(reversed(target)):
                result += pow(10, i) * crossed.index(x)

        # Return result
        return result

    def part_2_naive(self, data):
        return 0
        # Get all possible permutations
        permutations = np.asarray([
            list(permutation) for permutation in itertools.permutations('abcdefg')
        ])

        result = 0

        from tqdm import tqdm

        # Loop over all data
        for crossed, target in tqdm(data):
            # Loop over all permutations
            for permutation in permutations:
                # Check if the observation represents at least one digit for all observations
                if all(
                    # Check if permutation is correct
                    (self.digits == np.isin(permutation, observation)).all(axis=-1).any()
                    # Loop over all observations
                    for observation in crossed
                ):
                    subresult = ''
                    for digit in target:
                        digit = np.argwhere((self.digits == np.isin(permutation, digit)).all(axis=-1))[0][0]
                        subresult += str(digit)
                    result += int(subresult)

                    # Stop checking for other permutations
                    break

        # Return result
        return result
