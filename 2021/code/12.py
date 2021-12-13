import networkx as nx
import numpy    as np
from challenge import Challenge

class ChallengeSolution(Challenge):

    ########################################################################
    #                              Load data                               #
    ########################################################################

    def load(self, path):
        # Initialise graph
        graph = nx.Graph()

        # Load data from path
        with open(path) as infile:
            # Loop over lines
            for line in infile.readlines():
                # Get source target
                src, tgt = line.strip().split('-')
                # Add to graph
                graph.add_edge(src, tgt)

        # Return data
        return graph

    ########################################################################
    #                              Exercises                               #
    ########################################################################

    def part_1(self, graph):
        # Perform a depth first search
        return self.dfs(graph, 'start', 'end')


    def part_2(self, graph):
        # Perform a depth first search which can be visited twice
        return self.dfs2(graph, 'start', 'end')

    ########################################################################
    #           Minor rewrite of networkx all_simple_paths graph           #
    ########################################################################

    def dfs(self, graph, source, target, trace=None):
        """Perform depth first search over graph."""
        # Initialise result
        result = 0

        # Initialise trace if None
        if trace is None:
            trace = list()

        # If source == target, we are there!
        if source == target:
            return 1

        # Loop over all children of source
        for child in graph[source]:
            if child.isupper() or child not in trace:
                result += self.dfs(graph, child, target, trace + [source])

        # Return result
        return result

    def dfs2(self, graph, source, target, trace=None, small=None):
        """Perform depth first search over graph."""
        # Initialise result
        result = 0

        # Initialise trace if None
        if trace is None:
            trace = list()

        # If source == target, we are there!
        if source == target:
            return 1

        # Loop over all children of source
        for child in graph[source]:
            # Check if we can still visit child
            if child.isupper() or child not in trace:
                result += self.dfs2(graph, child, target, trace + [source], small=small)
            elif child in trace and small is None and child != 'start' and child != 'end':
                result += self.dfs2(graph, child, target, trace + [source], small=child)

        # Return result
        return result
