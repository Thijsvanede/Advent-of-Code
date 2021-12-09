import numpy as np
from day import Day

class Day7(Day):

    ########################################################################
    #                              Load data                               #
    ########################################################################

    def load(self, path):
        # Load data from path
        with open(path) as infile:
            data = np.asarray(list(map(int, infile.read().strip().split(','))))

        # Return data
        return data

    ########################################################################
    #                              Exercises                               #
    ########################################################################

    def part_1(self, data):
        # Part 1
        best_target = None
        best_cost   = float('inf')

        # Test each target position
        for target in range(data.min(), data.max() + 1):
            # Compute cost
            cost = np.sum(np.abs(data - target))
            # Print result
            if cost < best_cost:
                best_cost   = cost
                best_target = target

        # Return result
        return best_cost

    def part_2(self, data):
        # Compute cumulative sum
        cumsum = np.arange(data.max()+1).cumsum()

        best_target = None
        best_cost   = float('inf')

        # Test each target position
        for target in range(data.min(), data.max() + 1):
            # Compute cost
            cost = np.sum(cumsum[np.abs(data - target)])
            # Print result
            if cost < best_cost:
                best_cost   = cost
                best_target = target

        # Return result
        return best_cost
