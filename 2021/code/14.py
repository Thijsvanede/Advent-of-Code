import math
import numpy as np
from challenge   import Challenge
from collections import Counter

class ChallengeSolution(Challenge):

    ########################################################################
    #                              Load data                               #
    ########################################################################

    def load(self, path):
        # Load data from path
        with open(path) as infile:
            data, mapping = infile.read().split('\n\n')
            data    = data.strip()
            mapping = dict(
                pair.strip().split(' -> ')
                for pair in mapping.split('\n')
                if pair.strip()
            )

        # Return data
        return data, mapping

    ########################################################################
    #                              Exercises                               #
    ########################################################################

    def part_1(self, data):
        # Unpack data
        data, mapping = data

        # Perform given rounds
        for round in range(10):
            # Initialise buffer
            buffer = list()

            # Loop over all pairs
            for left, right in zip(data, data[1:]):
                # Get corresponding middle element
                middle = mapping[''.join((left, right))]
                # Append elements to buffer
                buffer.append(left)
                buffer.append(middle)

            # Append final element to buffer
            buffer.append(right)
            # Set data to buffer
            data = ''.join(buffer)

        # Get counts
        counts = list(sorted(Counter(data).items(), key=lambda x: x[1]))

        # Result is most frequent - least frequent
        return counts[-1][1] - counts[0][1]



    def part_2(self, data):
        # Unpack data
        data, mapping = data

        # Count pairs
        pairs = dict()
        for left, right in zip(data, data[1:]):
            if (left, right) not in pairs:
                pairs[(left, right)] = 0
            pairs[(left, right)] += 1

        # Loop over each round
        for round in range(40):
            # Set new counts
            counts = dict()

            # Loop over each pair
            for (left, right), count in pairs.items():
                # Get middle
                middle = mapping[''.join((left, right))]

                # Add counts if they do not yet exist
                if (left, middle) not in counts:
                    counts[(left, middle)] = 0
                if (middle, right) not in counts:
                    counts[(middle, right)] = 0

                # Add counts
                counts[(left  , middle)] += count
                counts[(middle, right )] += count

            # Set new counts
            pairs = counts

        # Initialise result
        result = dict()

        # Count total
        for (left, right), count in pairs.items():
            # Add items to result if it does not yet exist
            if left not in result:
                result[left] = 0
            if right not in result:
                result[right] = 0

            # Add counts
            result[left ] += count
            result[right] += count

        # Sort result
        result = list(sorted(result.items(), key=lambda x: x[1]))

        # Everything is counted twice, so result should be divided by 2
        result = [(character, math.ceil(count / 2)) for character, count in result]

        return result[-1][1] - result[0][1]
