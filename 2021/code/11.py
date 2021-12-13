import copy
import numpy as np
from challenge import Challenge

class ChallengeSolution(Challenge):

    ########################################################################
    #                              Load data                               #
    ########################################################################

    def load(self, path):
        # Load data from path
        with open(path) as infile:
            data = np.asarray([
                list(map(int, line.strip())) for line in infile.readlines()
            ])

        # Return data
        return data

    ########################################################################
    #                              Exercises                               #
    ########################################################################

    def part_1(self, data):
        # Set energy
        energy = copy.deepcopy(data)

        # Initialise result
        result = 0

        # Perform 100 rounds
        for round in range(100):
            # Increment energy
            energy += 1

            # Keep track of flashed items
            flashed = np.zeros(energy.shape, dtype=bool)
            flashes = np.logical_and(energy > 9, ~flashed)

            # Check if we have new flashes
            while np.any(flashes):
                # Perform flash in surrounding areas
                for x, y in np.argwhere(flashes):
                    for x_ in range(x-1, x+2):
                        for y_ in range(y-1, y+2):
                            if (
                                0 <= x_ < energy.shape[0] and
                                0 <= y_ < energy.shape[1] and
                                not (x_ == x and y_ == y)
                            ):
                                energy[x_, y_] += 1

                # Get new flashes
                flashed = np.logical_or(flashed, flashes)
                flashes = np.logical_and(energy > 9, ~flashed)


            # Reset energy to 0 where flashed
            energy[flashed] = 0

            # Add flashes to result
            result += np.sum(flashed)

        # Return result
        return result


    def part_2(self, data):
        # Set energy
        energy = copy.deepcopy(data)

        # Initialise result (iterations)
        result = 0

        while True:
            # Increment energy
            energy += 1

            # Keep track of flashed items
            flashed = np.zeros(energy.shape, dtype=bool)
            flashes = np.logical_and(energy > 9, ~flashed)

            # Check if we have new flashes
            while np.any(flashes):
                # Perform flash in surrounding areas
                for x, y in np.argwhere(flashes):
                    for x_ in range(x-1, x+2):
                        for y_ in range(y-1, y+2):
                            if (
                                0 <= x_ < energy.shape[0] and
                                0 <= y_ < energy.shape[1] and
                                not (x_ == x and y_ == y)
                            ):
                                energy[x_, y_] += 1

                # Get new flashes
                flashed = np.logical_or(flashed, flashes)
                flashes = np.logical_and(energy > 9, ~flashed)


            # Reset energy to 0 where flashed
            energy[flashed] = 0

            # Add flashes to result
            if np.all(flashed):
                return result + 1

            # Increment iteration
            result += 1
