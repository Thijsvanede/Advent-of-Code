import timeit

class Challenge(object):

    ########################################################################
    #                            Run challenge                             #
    ########################################################################

    def run(self, path):
        """Run challenge for a given day.

            Parameters
            ----------
            path : string
                Path to file from which to load data.
            """
        # Load data
        data = self.load(path)

        # Run part 1
        result_1 = self.part_1(data)
        print(f"Result part 1: {result_1}")

        # Run part 2
        result_2 = self.part_2(data)
        print(f"Result part 2: {result_2}")

    ########################################################################
    #                         Benchmark challenge                          #
    ########################################################################

    def benchmark(self, path, iterations=1_000, unit='s'):
        """Benchmark the different parts of the challenge."""
        # Load data
        data = self.load(path)

        # Time each part of the challenge
        time_1 = timeit.timeit(
            lambda: self.part_1(data),
            number = iterations,
        ) / iterations

        time_2 = timeit.timeit(
            lambda: self.part_2(data),
            number = iterations,
        ) / iterations

        # Adjust for unit
        if unit == 's':
            pass
        elif unit == 'ms':
            time_1 = time_1 * 1_000
            time_2 = time_2 * 1_000
        elif unit == 'micro':
            time_1 = time_1 * 1_000_000
            time_2 = time_2 * 1_000_000
            unit   = 'μs'
        else:
            raise ValueError(f"Unknown unit '{unit}'")

        # Output result
        print(f"Part 1 took {time_1} {unit} on average.")
        print(f"Part 2 took {time_2} {unit} on average.")

    ########################################################################
    #                              Load data                               #
    ########################################################################

    def load(self, path):
        """Load data for given AoC challenge from given path.

            Parameters
            ----------
            path : string
                Path to file from which to load data.

            Returns
            -------
            data : Object
                Data as loaded for exercise.
            """
        raise NotImplementedError(
            "Load method should be implemented seperately for each challenge."
        )

    ########################################################################
    #                          Exercise templates                          #
    ########################################################################

    def part_1(self, data):
        """Compute result of part 1 of AoC challenge.

            Parameters
            ----------
            data : Object
                Data as loaded by exercise.

            Returns
            -------
            result : Object
                Resulting computation of part 1 of AoC challenge.
            """
        raise NotImplementedError(
            "Part 1 should be implemented seperately for each challenge."
        )

    def part_2(self, data):
        """Compute result of part 2 of AoC challenge.

            Parameters
            ----------
            data : Object
                Data as loaded by exercise.

            Returns
            -------
            result : Object
                Resulting computation of part 2 of AoC challenge.
            """
        raise NotImplementedError(
            "Part 2 should be implemented seperately for each challenge."
        )
