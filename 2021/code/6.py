import numpy as np
from day import Day

class Day6(Day):

    ########################################################################
    #                              Load data                               #
    ########################################################################

    def load(self, path):
        # Read data
        with open(path) as infile:
            data = np.asarray(list(map(int, infile.read().strip().split(','))))

        # Return data
        return data

    ########################################################################
    #                              Exercises                               #
    ########################################################################

    def part_1(self, data):
        # Count fish counters
        counts = [np.sum(data == count) for count in range(9)]

        # Run for 80 iterations
        for i in range(80):
            new = counts[0]
            counts = counts[1:] + [new]
            counts[6] += new

        # Return result
        return np.asarray(counts).sum()

    def part_2(self, data):
        # Count fish counters
        counts = [np.sum(data == count) for count in range(9)]

        # Run for 256 iterations
        for i in range(256):
            new = counts[0]
            counts = counts[1:] + [new]
            counts[6] += new

        # Return result
        return np.asarray(counts).sum()
