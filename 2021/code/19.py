from challenge import Challenge
import itertools
import numpy as np
import re

class ChallengeSolution(Challenge):

    ########################################################################
    #                              Load data                               #
    ########################################################################

    def load(self, path):
        # Initialise result
        result = list()

        # Load data from path
        with open(path) as infile:
            # Read lines
            for scanner in re.split('--- scanner \d+ ---', infile.read()):
                if scanner.strip():
                    # Get reading
                    result.append(np.asarray([
                        list(map(int, scan.split(',')))
                        for scan in scanner.strip().split('\n')
                        if scan.strip()
                    ]))

        # Return result
        return result

    ########################################################################
    #                              Exercises                               #
    ########################################################################

    def part_1(self, scanners):
        # Initialise beacons from scanner 0
        beacons = scanners[0]
        # Initialise list of scanners that have been visited
        visited = np.zeros(len(scanners), dtype=bool)
        visited[0] = True

        # Initialise manhattan distances
        self.coordinates = np.zeros((len(scanners), 3), dtype=int)

        # Loop until we added all scanners
        while not np.all(visited):

            # Loop over all scanners
            for index, scanner in enumerate(scanners):
                if visited[index]: continue

                # Get all rotations of scanner
                for scanner_ in self.orientations(scanner):
                    # Compare scanner with beacons
                    difference = self.difference(beacons, scanner_)

                    # Flatten difference
                    difference_ = difference.reshape(-1, 3)
                    # Get unique diffs
                    unique, counts = np.unique(
                        difference_,
                        return_counts = True,
                        axis          = 0,
                    )

                    # Check if we found more than 12 times the same difference
                    if np.any(counts >= 12):
                        # Get indices in original
                        indices = np.argwhere(np.all(
                            difference == unique[counts >= 12][0],
                            axis = 2,
                        ))


                        # Get indices for beacons and scanner
                        indices_beacons = indices[:, 0]
                        indices_scanner = indices[:, 1]

                        # Assert we have a large enough overlap
                        assert np.unique(indices_beacons).shape[0] >= 12

                        # Get relative difference
                        difference = unique[counts >= 12][0]
                        self.coordinates[index] = difference

                        # Transpose scanner using difference
                        scanner_ += difference

                        # Add scanner to beacons
                        beacons = np.asarray([list(beacon) for beacon in
                            set([tuple(beacon) for beacon in beacons ]) |
                            set([tuple(beacon) for beacon in scanner_])
                        ])

                        # Pop scanner
                        visited[index] = True

        return beacons.shape[0]

    def part_2(self, data):
        """Return max distance as computed by 1"""
        # Compute difference between all scanner coordinates
        difference = self.difference(self.coordinates, self.coordinates)
        # Return maximum manhattan difference
        return np.abs(difference).sum(axis=-1).max()

    ########################################################################
    #                           Compare scanners                           #
    ########################################################################

    def difference(self, a, b):
        """Get the difference between a and b."""
        return a[:, np.newaxis, :] - b[np.newaxis, :, :]

    ########################################################################
    #                        Orientation functions                         #
    ########################################################################

    def orientations(self, scanner):
        """Return scanner orientations over X."""
        # Rotate face
        for face in self.rotate_face(scanner):
            # Rotate degrees
            yield from self.rotate_90(face)

    def rotate_90(self, scanner):
        """Rotate scanner by 90 degrees."""
        yield scanner
        for i in range(3):
            scanner = scanner[:, [0, 2, 1]] * [1, 1, -1]
            yield scanner

    def rotate_face(self, scanner):
        """Rotate face of scanner in 1 of 6 positions."""
        yield scanner
        yield scanner[:, [1, 0, 2]] * [ 1, -1,  1]
        yield scanner[:, [0, 1, 2]] * [-1, -1,  1]
        yield scanner[:, [1, 0, 2]] * [-1,  1,  1]
        yield scanner[:, [2, 1, 0]] * [-1,  1,  1]
        yield scanner[:, [2, 1, 0]] * [ 1,  1, -1]
