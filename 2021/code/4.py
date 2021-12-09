import numpy as np
from day import Day

class Day4(Day):

    ########################################################################
    #                              Load data                               #
    ########################################################################

    def load(self, path):
        # Read board
        with open(path) as infile:
            # Read numbers and boards separately
            numbers, *boards = infile.read().split('\n\n')

        # Cast numbers to array
        numbers = np.asarray(list(map(int, numbers.split(','))))

        # Cast boards to array
        boards = np.asarray([
            list(map(int, board.split())) for board in boards
        ]).reshape(-1, 5, 5)

        # Return result
        return numbers, boards

    ########################################################################
    #                              Exercises                               #
    ########################################################################

    def part_1(self, data):
        # Unpack data
        numbers, boards = data

        # Keep track of crossed off numbers
        crossed = np.zeros(boards.shape, dtype=bool)

        # Call out numbers one at the time
        for number in numbers:
            # Cross off number at all bingo boards
            crossed[boards == number] = True

            # Check if there is a winner
            vertical   = crossed.sum(axis=1) == crossed.shape[1]
            horizontal = crossed.sum(axis=2) == crossed.shape[2]

            # Check vertical and horizontal boards for winners
            for check in [vertical, horizontal]:

                # Perform check
                if np.any(check):
                    # Get index of winning board
                    board = np.argwhere(check)[0, 0]
                    # Compute score
                    score = np.sum(boards[board][~crossed[board]]) * number
                    # Stop bingo because we have a winner
                    break
            else: continue
            break

        # Print score
        return score


    def part_2(self, data):
        # Unpack data
        numbers, boards = data

        # Keep track of crossed off numbers
        crossed          = np.zeros(boards.shape   , dtype=bool)
        previous_winners = np.zeros(boards.shape[0], dtype=bool)

        # Call out numbers one at the time
        for number in numbers:
            # Cross off number at all bingo boards
            crossed[boards == number] = True

            # Check if there is a winner
            vertical   = crossed.sum(axis=1) == crossed.shape[1]
            horizontal = crossed.sum(axis=2) == crossed.shape[2]

            # Check vertical and horizontal boards for winners
            for check in [vertical, horizontal]:

                # Perform check
                if np.any(check):
                    # Get winners
                    winners = np.logical_or(
                        previous_winners,
                        np.any(check, axis=1),
                    )
                    # Check if there is a single board remaining
                    if winners.shape[0] == winners.sum():
                        # Get last winning board
                        board = np.flatnonzero(~previous_winners)[0]
                        # Compute score
                        score = np.sum(boards[board][~crossed[board]]) * number
                        # Stop bingo because we have a winner
                        break

                    # Set previous winners
                    previous_winners = np.logical_or(
                        np.any(check, axis=1),
                        previous_winners,
                    )
            else: continue
            break


        # Print score
        return score
