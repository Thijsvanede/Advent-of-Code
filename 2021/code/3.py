import copy
import numpy as np
from challenge import Challenge

class ChallengeSolution(Challenge):

    ########################################################################
    #                              Load data                               #
    ########################################################################

    def load(self, path):
        # Open path
        with open(path) as infile:
            # Read bits as integers
            data = np.asarray([
                list(map(int, line.strip()))
                for line in infile.readlines()
            ])

        # Return data
        return data

    ########################################################################
    #                              Exercises                               #
    ########################################################################

    def part_1(self, data):
        # Count bits in each column
        ones  = np.count_nonzero(data, axis=0)
        zeros = data.shape[0] - ones

        gamma   = np.where(ones > zeros, 1, 0)
        epsilon = np.where(ones < zeros, 1, 0)

        gamma   = int(''.join(str(x) for x in gamma  ), 2)
        epsilon = int(''.join(str(x) for x in epsilon), 2)

        # Return result
        return gamma * epsilon


    def part_2(self, data):
        oxygen = copy.deepcopy(data)
        co2    = copy.deepcopy(data)

        for i in range(data.shape[1]):
            column = oxygen[:, i]

            if oxygen.shape[0] == 1:
                break

            if np.count_nonzero(column) >= oxygen[:, i].shape[0] / 2:
                oxygen = oxygen[column == 1]
            else:
                oxygen = oxygen[column == 0]

        for i in range(data.shape[1]):
            column = co2[:, i]

            if co2.shape[0] == 1:
                break

            if np.count_nonzero(column) < co2[:, i].shape[0] / 2:
                co2 = co2[column == 1]
            else:
                co2 = co2[column == 0]

        oxygen = int(''.join(str(x) for x in oxygen[0]), 2)
        co2    = int(''.join(str(x) for x in co2[0]   ), 2)

        # Return result
        return oxygen * co2
