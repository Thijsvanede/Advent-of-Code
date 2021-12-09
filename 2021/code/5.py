import numpy as np
from day import Day

class Day5(Day):

    ########################################################################
    #                              Load data                               #
    ########################################################################

    def load(self, path):
        # Read input
        with open(path) as infile:
            # Initialise lines
            lines = list()

            # Read lines from file
            for line in infile.readlines():
                src, dst = line.strip().split(' -> ')
                x1, y1   = map(int, src.split(','))
                x2, y2   = map(int, dst.split(','))

                lines.append([x1, y1, x2, y2])

        # Cast to array and return
        return np.asarray(lines)

    ########################################################################
    #                              Exercises                               #
    ########################################################################

    def part_1(self, lines):
        # Initialise diagram for lines
        diagram = np.zeros((
            max(lines[:, 0].max(), lines[:, 2].max()) + 1,
            max(lines[:, 1].max(), lines[:, 3].max()) + 1,
        ), dtype=int)

        # Loop over all lines
        for x1, y1, x2, y2 in lines:
            # Add horizontal lines
            if x1 == x2:
                diagram[x1, min(y1, y2):max(y1, y2) + 1] += 1
            # Add vertial lines
            elif y1 == y2:
                diagram[min(x1, x2):max(x1, x2) + 1, y1] += 1

        # Return number of dangerous areas
        return np.sum(diagram >= 2)

    def part_2(self, lines):
        # Initialise diagram for lines
        diagram = np.zeros((
            max(lines[:, 0].max(), lines[:, 2].max()) + 1,
            max(lines[:, 1].max(), lines[:, 3].max()) + 1,
        ), dtype=int)

        # Loop over all lines
        for x1, y1, x2, y2 in lines:
            # Add horizontal lines
            if x1 == x2:
                diagram[x1, min(y1, y2):max(y1, y2) + 1] += 1
            # Add vertial lines
            elif y1 == y2:
                diagram[min(x1, x2):max(x1, x2) + 1, y1] += 1
            # Add diagonal lines
            else:
                # Get low and high numbers
                x_low  = min(x1, x2)
                x_high = max(x1, x2)
                y_low  = min(y1, y2)
                y_high = max(y1, y2)

                # Define ranges
                x = np.arange(x_low, x_high + 1)
                y = np.arange(y_low, y_high + 1)

                if (x1 == x_low and y1 == y_low) or (x2 == x_low and y2 == y_low):
                    diagram[x, y] += 1
                else:
                    diagram[x[::-1], y] += 1

        # Return number of dangerous areas
        return np.sum(diagram >= 2)
