import argformat
import argparse
import importlib

if __name__ == "__main__":
    ########################################################################
    #                           Parse arguments                            #
    ########################################################################

    # Parse arguments
    parser = argparse.ArgumentParser(
        description     = "Run AoC exercises",
        formatter_class = argformat.StructuredFormatter,
    )

    # Optional arguments
    parser.add_argument(
        "days",
        nargs = '+',
        help  = "AoC day(s) for which to run exercise",
    )

    parser.add_argument(
        "--benchmark",
        type    = int,
        default = 0,
        help    = "benchmark to run for given number of iterations",
    )
    parser.add_argument(
        "--unit",
        choices = ('s', 'ms', 'micro'),
        default = 's',
        help = "unit to use for benchmark",
    )

    parser.add_argument(
        "--test",
        action = 'store_true',
        help = "if given, use test data",
    )

    # Parse arguments
    args = parser.parse_args()

    ########################################################################
    #                            Run challenge                             #
    ########################################################################

    # Loop over all days
    for day in args.days:
        # Print header
        print("#"*80)
        print("#{:^78}#".format("Day {}".format(day)))
        print("#"*80)
        print()

        # Load challenge object
        challenge = getattr(importlib.import_module(f"{day}"), f"Day{day}")()

        # Get path for specific day
        if args.test:
            path = f"test/{day}.txt"
        else:
            path = f"data/{day}.txt"

        # Run challenge
        challenge.run(path)

        # If required, run benchmark
        if args.benchmark:
            challenge.benchmark(path, iterations=args.benchmark, unit=args.unit)

        # Print footer
        print()
