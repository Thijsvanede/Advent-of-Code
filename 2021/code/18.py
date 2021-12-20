from challenge import Challenge
import copy
import itertools
import math
import random

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
            for line in infile.readlines():
                # Transform to graph and append to result
                result.append(SnailFishNumber.from_list(eval(line)))

        # Return result
        return result

    ########################################################################
    #                              Exercises                               #
    ########################################################################

    def part_1(self, data):
        # Copy data
        data = copy.deepcopy(data)
        # Initialise result
        result = data[0]

        # Add graphs to result
        for snailfish_number in data[1:]:
            # Add graphs together
            result += snailfish_number
            # Reduce result
            result = result.reduce()

        # Return magnitude of result
        return result.magnitude()

    def part_2(self, data):
        # Initialise result
        result = -float('inf')

        # Get all permutations of length 2
        for a, b in itertools.permutations(data, 2):
            # Set result to maximum magnitude
            result = max(result, (a + b).reduce().magnitude())

        # Return result
        return result

    ########################################################################
    #                         Auxiliary functions                          #
    ########################################################################

class SnailFishNumber(object):

    def __init__(self, graph):
        # Initialise graph
        self.graph = graph

    ########################################################################
    #                             Properties                               #
    ########################################################################

    def magnitude(self, graph=None):
        """Compute magnitude of graph"""
        # Use self.graph if not given
        if graph is None:
            graph = self.graph

        # Initialise result
        result = 0

        # Add left to result
        if isinstance(graph['left'], int):
            result += 3 * graph['left']
        else:
            result += 3 * self.magnitude(graph['left'])

        # Add right to result
        if isinstance(graph['right'], int):
            result += 2 * graph['right']
        else:
            result += 2 * self.magnitude(graph['right'])

        # Return result
        return result

    ########################################################################
    #                               Methods                                #
    ########################################################################

    def reduce(self):
        """Reduce a snailfish number represented by graph."""
        # Explode
        self.graph, changed = self.explode(self.graph)

        # Iterate through graph until nothing explodes
        while changed:
            # Explode
            self.graph, changed = self.explode(self.graph)

        # Explode
        self.graph, changed = self.split(self.graph)

        # Perform reduce again
        if changed:
            return self.reduce()

        # Return self
        return self


    def explode(self, graph):
        """Explode graph at depth 4."""
        # Get graph leafs
        leafs = list(self.iterate_leafs(graph))

        # Explode leafs of given depth
        for index, (leaf, depth, path) in enumerate(leafs):
            # Check if depth is 4 and we are working with a pair
            if (
                depth == 4 and
                isinstance(self.get_nested(graph, path[:-1])['left' ], int) and
                isinstance(self.get_nested(graph, path[:-1])['right'], int)
            ):
                # Explode left
                if index > 0:
                    # Set entry of next left node
                    self.set_nested(
                        graph,
                        leafs[index-1][2],
                        self.get_nested(graph, leafs[index-1][2]) +
                        self.get_nested(graph, path[:-1])['left' ],
                    )

                # Explode right
                if index < len(leafs)-2:
                    # Get entry of next right node
                    self.set_nested(
                        graph,
                        leafs[index+2][2],
                        self.get_nested(graph, leafs[index+2][2]) +
                        self.get_nested(graph, path[:-1])['right' ],
                    )

                # Set to 0
                self.set_nested(graph, path[:-1], 0)

                # Return graph
                return graph, True

        # Return graph
        return graph, False


    def split(self, graph, threshold=10):
        """Split a number if it is >= than the given threshold."""
        for leaf, depth, path in self.iterate_leafs(graph):
            # Check if we should split
            if leaf >= threshold:

                # Perform split
                self.set_nested(graph, path, {
                    "left" : math.floor(leaf / 2),
                    "right": math.ceil (leaf / 2),
                })

                # Return graph
                return graph, True

        # Return graph
        return graph, False

    ########################################################################
    #                              Iterators                               #
    ########################################################################

    def iterate_leafs(self, graph, depth=-1, path=tuple()):
        """Iterate over all integers in graph, sorted"""
        if (isinstance(graph, int)):
            yield graph, depth, path
        else:
            yield from self.iterate_leafs(graph.get('left' , {}), depth+1, path + ('left' ,))
            yield from self.iterate_leafs(graph.get('right', {}), depth+1, path + ('right',))

    def get_nested(self, graph, keys):
        """Get value from nested dictionary"""
        # Perform nested search
        for key in keys:
            graph = graph[key]
        # Return result
        return graph

    def set_nested(self, graph, keys, value):
        """Set value in nested dictionary."""
        # Perform nested trace
        for key in keys[:-1]:
            graph = graph[key]
        # Set result
        graph[keys[-1]] = value


    ########################################################################
    #                           Method overrides                           #
    ########################################################################

    def __add__(self, other):
        """Add two graphs together."""
        if not isinstance(other, SnailFishNumber):
            raise TypeError("Can only add together SnailFishNumbers")

        # Return new SnailFishNumber
        return SnailFishNumber({
            "left" : copy.deepcopy(self .graph),
            "right": copy.deepcopy(other.graph),
        })

    def __radd__(self, other):
        """Add two graphs together."""
        # Check SnailFishNumber
        if not isinstance(other, SnailFishNumber):
            raise TypeError("Can only add together SnailFishNumbers")

        # Return addition
        return self + other

    ########################################################################
    #                             I/O methods                              #
    ########################################################################

    @classmethod
    def from_list(cls, data):
        return cls(SnailFishNumber.to_graph(data))


    def to_list(self, graph=None):
        """Transform SnailFishNumber to list."""
        if graph is None:
            graph = self.graph

        if isinstance(graph, int):
            return graph
        else:
            return [
                self.to_list(graph.get('left' )),
                self.to_list(graph.get('right')),
            ]


    @staticmethod
    def to_graph(data):
        """Transform data to graph."""
        # Initialise graph
        graph = dict()

        # Ensure length is 2
        assert len(data) == 2, "Expected 2 items"

        # Left child
        if isinstance(data[0], int):
            graph['left'] = data[0]
        else:
            graph['left'] = SnailFishNumber.to_graph(data[0])

        # Right child
        if isinstance(data[1], int):
            graph['right'] = data[1]
        else:
            graph['right'] = SnailFishNumber.to_graph(data[1])

        # Return graph
        return graph


    def __str__(self):
        """Return string representation of number."""
        return str(self.to_list()).replace(' ', '')
