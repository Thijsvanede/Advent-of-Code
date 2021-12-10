import argformat
import argparse
import importlib
import os

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
        "--days",
        nargs   = '+',
        default = ['all'],
        help    = "run exercise for given days. can be 'all', <int> [<int> ...], <start>-<stop>",
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

    # Parse days
    if len(args.days) == 1 and args.days[0] == 'all':
        # Initialise days
        args.days = list()

        # Loop over all implemented solutions
        for solution in os.listdir("code"):
            # Get potential solution
            solution = os.path.splitext(solution)[0]
            # Check if solution is number
            if solution.isdigit():
                # Add solution
                args.days.append(int(solution))

        # Sort by day
        args.days = sorted(args.days)

    elif len(args.days) == 1 and '-' in args.days[0]:
        # Get range
        start, end = args.days[0].split('-', 1)
        start = int(start) if start else 1
        end   = int(end)+1 if end   else 26
        args.days = range(start, end)

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
        challenge = getattr(importlib.import_module(f"{day}"), "ChallengeSolution")()

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
