import networkx as nx
import numpy    as np
from challenge import Challenge

class ChallengeSolution(Challenge):

    ########################################################################
    #                              Load data                               #
    ########################################################################

    def load(self, path):
        # Load data from path
        with open(path) as infile:
            # Read infile
            points, folds = infile.read().split('\n\n')

            # Parse points
            points = np.asarray([
                list(map(int, point.split(','))) for point in points.split()
            ])

            # Parse folds
            folds = [
                fold.strip().split('=') for fold in folds.split('\n') if fold
            ]
            folds = [(xy[-1], int(fold)) for xy, fold in folds]

        # Return data
        return points, folds

    ########################################################################
    #                              Exercises                               #
    ########################################################################

    def part_1(self, data):
        # Unpack folds and points
        points, folds = data

        # Create array by points
        result = np.zeros((
            points[:, 1].max()+1,
            points[:, 0].max()+1,
        ), dtype=bool)

        # Set points
        result[points[:, 1], points[:, 0]] = True

        # Perform fold
        for xy, fold in folds:
            # Case of y fold
            if xy == 'y':
                # Get two parts of fold
                a = result[:fold]
                b = result[fold+1:]

                # Perform fold
                result = np.logical_or(a, b[::-1])

            # Case of x fold
            elif xy == 'x':
                # Get two parts of fold
                a = result[:, :fold]
                b = result[:, fold+1:]

                # Perform fold
                result = np.logical_or(a, b.T[::-1].T)

            return result.sum()


    def part_2(self, data):
        # Unpack folds and points
        points, folds = data

        # Create array by points
        result = np.zeros((
            points[:, 1].max()+1,
            points[:, 0].max()+1,
        ), dtype=bool)

        # Set points
        result[points[:, 1], points[:, 0]] = True

        # Perform fold
        for xy, fold in folds:
            # Case of y fold
            if xy == 'y':
                # Get two parts of fold
                a = result[:fold]
                b = result[fold+1:]

                # Perform fold
                result = np.logical_or(a, b[::-1])

            # Case of x fold
            elif xy == 'x':
                # Get two parts of fold
                a = result[:, :fold]
                b = result[:, fold+1:]

                # Perform fold
                result = np.logical_or(a, b.T[::-1].T)

        # Show result
        return self.show(result)


    def show(self, result):
        string = ''
        for row in result:
            string += '\n' + ''.join(['█' if item else ' ' for item in row])
        return string
