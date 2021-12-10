import numpy as np
from challenge import Challenge

class ChallengeSolution(Challenge):

    ########################################################################
    #                              Load data                               #
    ########################################################################

    def load(self, path):
        # Load data from path
        with open(path) as infile:
            data = np.asarray(list(map(int, infile.readlines())))

        # Return data
        return data

    ########################################################################
    #                              Exercises                               #
    ########################################################################

    def part_1(self, data):
        # Compute number of increases
        diff = np.diff(data)
        # Return number of positive increases
        return (diff > 0).sum()

    def part_2(self, data):
        # Average 3 time measurement
        depth = np.asarray(data[:-2] + data[1:-1] + data[2:])
        # Compute number of increases
        diff  = np.diff(depth)
        # Return number of positive increases
        return (diff > 0).sum()
