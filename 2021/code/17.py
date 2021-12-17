from challenge import Challenge

class ChallengeSolution(Challenge):

    ########################################################################
    #                              Load data                               #
    ########################################################################

    def load(self, path):
        # Load data from path
        with open(path) as infile:
            x, y = infile.read().strip()[15:].split(', y=')
            x_start, x_end = map(int, x.split('..'))
            y_start, y_end = map(int, y.split('..'))

        # Return data
        return (x_start, x_end, min(y_start, y_end), max(y_start, y_end))

    ########################################################################
    #                              Exercises                               #
    ########################################################################

    def part_1(self, data):
        # Initialise result
        result = -float('inf')

        # Unpack data
        x_start, x_end, y_start, y_end = data

        # Get horizontal steps for each value of x
        horizontal_steps = {
            x: self.horizontal_steps(x, x_start, x_end) for x in range(x_end+1)
        }

        # Loop over all possible horizontal steps
        for x, steps in horizontal_steps.items():
            # Loop over all possible steps
            for step in steps:
                # Check if steps is integer
                if isinstance(step, int):
                    y = self.vertical_steps(step, y_start, y_end, False)
                elif step == '...':
                    y = self.vertical_steps(steps[-2], y_start, y_end, True)
                else:
                    raise ValueError(f"Unknown number of steps '{step}'.")

                # Compute highest number of steps
                for velocity, n_steps in y:
                    result = max(result, self.highest_point(velocity, n_steps))

        # Return result
        return result

    def part_2(self, data):
        # Initialise result
        result = set()

        # Unpack data
        x_start, x_end, y_start, y_end = data

        # Get horizontal steps for each value of x
        horizontal_steps = {
            x: self.horizontal_steps(x, x_start, x_end) for x in range(x_end+1)
        }

        # Loop over all possible horizontal steps
        for x, steps in horizontal_steps.items():
            # Loop over all possible steps
            for step in steps:
                # Check if steps is integer
                if isinstance(step, int):
                    y = self.vertical_steps(step, y_start, y_end, False)
                elif step == '...':
                    y = self.vertical_steps(steps[-2], y_start, y_end, True)
                else:
                    raise ValueError(f"Unknown number of steps '{step}'.")

                # Compute highest number of steps
                result |= set([(x, y[0]) for y in y])

        # Return result
        return len(result)


    ########################################################################
    #                         Auxiliary functions                          #
    ########################################################################

    def horizontal_steps(self, x, start, end):
        """Compute possible number of horizontal steps to reach target area.

            Parameters
            ----------
            x : int
                Initial x velocity.

            start : int
                Minimal target area (inclusive).

            end : int
                Maximal target area (inclusive).

            Returns
            -------
            result : list()
                List of number of steps for given x to fall within target area.
            """
        # Initialise result
        result = list()

        # Set velocity
        velocity = x
        # Set distance
        distance = 0
        # Set steps
        steps = 0

        # Loop until distance is too big
        while velocity > 0 and distance <= end:
            # Add steps if necessary
            if distance >= start:
                result.append(steps)

            # Add number of steps
            distance += velocity
            velocity = max(0, velocity-1)
            steps    += 1

        # Case where we come to a standstill within the target area x
        if result and velocity == 0:
            result.append('...')

        # Return result
        return result


    def vertical_steps(self, steps, start, end, infinity=False):
        """Compute possible values for y to reach target area in given number
            of steps.

            Parameters
            ----------
            steps : int or '...'
                Number of steps that y can take.

            start : int
                Minimal target area (inclusive).

            end : int
                Maximal target area (inclusive).

            infinity : boolean, default=False
                If True, allow any number of> steps: [steps+1, ...).
            """
        # Initialise result
        result = list()

        # Initialise y
        y = start

        # Loop until break
        while y < 200: # TODO: 200 is super arbitrary, should fix

            # Set velocity
            velocity = y
            # Set distance
            distance = 0

            # Compute number of steps
            for _ in range(steps):
                # Increment distance
                distance += velocity
                # Decrese velocity
                velocity -= 1

            # Add y if distance is correct
            if start <= distance <= end:
                result.append((y, steps))

            # Case for infinity
            if infinity:

                # Take additional steps until distance is out of range
                while distance > end:
                    # Increment steps
                    steps += 1
                    # Increment distance
                    distance += velocity
                    # Decrese velocity
                    velocity -= 1

                    # Add y if distance is correct
                    if start <= distance <= end:
                        result.append((y, steps))

            # Increment y
            y += 1

        # Return result
        return result


    def highest_point(self, y, steps):
        """Compute the highest point reached by y in given number of steps."""
        # Initialise result
        result = 0

        # Initialise height and velocity
        height   = 0
        velocity = y

        # Loop over given number of steps
        for step in range(steps):
            # Increment height and decrement velocity
            height   += velocity
            velocity -= 1

            # Set result to maximum
            result = max(height, result)

        # Return result
        return result
