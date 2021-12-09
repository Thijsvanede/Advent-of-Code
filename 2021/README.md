# Advent of Code 2021
Implementations for the Advent of Code 2021 challenges.

## Organisation
This directory contains 3 subdirectories:
 *. `code/`, contains the implementations for each Advent of Code challenge per day.
 *. `data/`, contains the data provided for each Advent of Code challenge per day.
 *. `test/`, contains the test data provided for each Advent of Code challenge per day.

For each day, this repository contains the following:
 *. `code/{day}.py`, implementing the challenge for that day.
 *. `data/{day}.txt`, containing the data for that day.
 *. `test/{day}.txt`, containing the test data for that day.

## Framework
Each Advent of Code is implemented using the framework provided in `code/day.py`.
This means that each day implements the following methods:
```python
from day import Day

class Day{day}(Day):
    """Implementation of day."""

    def load(self, path):
        """Loads data from given path."""
        pass

    def part_1(self, data):
        """Computes part_1 of challenge for given day using loaded data."""
        pass

    def part_2(self, data):
        """Computes part_2 of challenge for given day using loaded data."""
        pass
```

The `Day` class from `code/day.py` uses this generic API to provide automated running of the challenge per day, as well as benchmarking the solutions for each part of the day to provide a time indication.

## Usage
To run the e.g., day `X` implemented in this repository, simply run `python3 code X` from this directory.

### Help
```
usage: code [-h] [--benchmark BENCHMARK] [--unit {s,ms,micro}] [--test] days [days ...]

Run AoC exercises

positional arguments:
  days                   AoC day(s) for which to run exercise

optional arguments:
  -h, --help             show this help message and exit
  --benchmark BENCHMARK  benchmark to run for given number of iterations
  --unit {s,ms,micro}    unit to use for benchmark                       (default = s)
  --test                 if given, use test data
```
