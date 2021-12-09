import numpy as np
from day import Day

class Day9(Day):

    ########################################################################
    #                              Load data                               #
    ########################################################################

    def load(self, path):
        # Load data from path
        with open(path) as infile:
            data = np.asarray([
                list(map(int, x.strip())) for x in infile.readlines()
            ])

        # Return data
        return data

    ########################################################################
    #                              Exercises                               #
    ########################################################################

    def part_1(self, height):
        # Initialise lowest
        self.lowest = np.ones(height.shape, dtype=bool)

        # Compute lowest points
        self.lowest[1:     ] = np.logical_and(self.lowest[1:     ], height[1:     ] < height[ :-1   ]) # Right
        self.lowest[  :-1  ] = np.logical_and(self.lowest[ :-1   ], height[ :-1   ] < height[1:     ]) # Left
        self.lowest[:, 1:  ] = np.logical_and(self.lowest[:, 1:  ], height[:, 1:  ] < height[:,  :-1]) # Down
        self.lowest[:,  :-1] = np.logical_and(self.lowest[:,  :-1], height[:,  :-1] < height[:, 1:  ]) # Up

        # Return result
        return np.sum(height[self.lowest] + 1)

    def part_2(self, height):
        # Find basins
        basins = np.full(height.shape, -1, dtype=int)

        # Get coordinates of each low point
        for basin, (x, y) in enumerate(np.argwhere(self.lowest)):
            # Fill basin
            basins = self.fill_basin(basins, height, x, y, basin)

        # Get size of basins
        sizes = np.unique(basins, return_counts=True)[1][1:]
        # Find size of 3 largest basins
        largest = np.sort(sizes)[-3:]

        # Get result and return
        return largest[0] * largest[1] * largest[2]

    ########################################################################
    #                         Auxiliary functions                          #
    ########################################################################

    def fill_basin(self, basins, height, x, y, basin):
        # Check if basin should be filled
        if (
            0 <= x < basins.shape[0] and
            0 <= y < basins.shape[1] and
            basins[x, y] != basin and
            height[x, y] != 9
        ):

            # Check if basin was already filled
            if basins[x, y] != -1: raise ValueError("Basin already filled!")

            # Fill basin
            basins[x, y] = basin

            # Fill surrounding basins
            basins = self.fill_basin(basins, height, x-1, y, basin)
            basins = self.fill_basin(basins, height, x+1, y, basin)
            basins = self.fill_basin(basins, height, x, y-1, basin)
            basins = self.fill_basin(basins, height, x, y+1, basin)

        # Return basins
        return basins
