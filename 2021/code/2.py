import numpy as np
from challenge import Challenge

class ChallengeSolution(Challenge):

    ########################################################################
    #                              Load data                               #
    ########################################################################

    def load(self, path):
        # Open file
        with open(path) as infile:
            instructions = list()
            data         = list()

            for line in infile.readlines():
                instruction, datum = line.split()
                instructions.append(instruction)
                data        .append(int(datum))

        # Add instructions and data
        instructions = np.asarray(instructions)
        data         = np.asarray(data)

        # Return result
        return data, instructions

    ########################################################################
    #                              Exercises                               #
    ########################################################################

    def part_1(self, data):
        # Unpack data
        data, instructions = data

        # Compute number of total horizontal steps forward
        horizontal = data[instructions == 'forward'].sum()
        # Compute number of vertical steps
        depth = data[instructions == 'down'].sum() -\
                data[instructions == 'up'  ].sum()

        # Multiply horizontal and depth to get result
        return horizontal * depth

    def part_2(self, data):
        # Unpack data
        data, instructions = data

        horizontal = 0
        aim        = 0
        depth      = 0

        for instruction, datum in zip(instructions, data):
            if instruction == "down":
                aim += datum
            elif instruction == "up":
                aim -= datum
            elif instruction == "forward":
                horizontal += datum
                depth += aim * datum

        # Multiply horizontal and depth to get result
        return horizontal * depth
