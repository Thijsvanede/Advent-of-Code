import networkx as nx
import numpy    as np
import scipy    as sp
from challenge import Challenge


class ChallengeSolution(Challenge):

    ########################################################################
    #                              Load data                               #
    ########################################################################

    def load(self, path):
        # Load data from path
        with open(path) as infile:
            data = np.asarray([
                list(map(int, line.strip()))
                for line in infile.readlines() if line.strip()
            ])

        # Return data
        return data

    ########################################################################
    #                              Exercises                               #
    ########################################################################

    def part_1(self, data):
        # Get input as graph
        graph = self.to_graph(data)

        # Compute shortest path
        return int(sp.sparse.csgraph.shortest_path(graph, indices=0)[-1])


    def part_2(self, data):
        # Create different parts
        parts = np.asarray([data]*9) + np.arange(9).reshape(-1, 1, 1)
        parts[parts > 9] = np.mod(parts[parts > 9], 9)

        # Create new array
        data = np.concatenate([
            np.concatenate(parts[i:i+5]) for i in range(5)
        ], axis=1)

        # Compute graph
        graph = self.to_graph(data)

        # Compute shortest path
        return int(sp.sparse.csgraph.shortest_path(graph, indices=0)[-1])


    ########################################################################
    #                          Auxiliary methods                           #
    ########################################################################

    def to_graph(self, data):
        """Create a scipy.sparse graph from the adjacency matrix."""
        # Get identifiers for each point in graph
        identifiers = np.arange(
            data.shape[0] * data.shape[1]
        ).reshape(data.shape[0], data.shape[1])

        # S -> N
        src_sn    = identifiers[1:  ].reshape(-1)
        dst_sn    = identifiers[ :-1].reshape(-1)
        weight_sn = data       [ :-1].reshape(-1)

        # N -> S
        src_ns    = identifiers[ :-1].reshape(-1)
        dst_ns    = identifiers[1:  ].reshape(-1)
        weight_ns = data[1:  ].reshape(-1)

        # W -> E
        src_we    = identifiers[:,  :-1].reshape(-1)
        dst_we    = identifiers[:, 1:  ].reshape(-1)
        weight_we = data       [:, 1:  ].reshape(-1)

        # E -> W
        src_ew    = identifiers[:, 1:  ].reshape(-1)
        dst_ew    = identifiers[:,  :-1].reshape(-1)
        weight_ew = data       [:,  :-1].reshape(-1)

        src    = np.concatenate((src_sn   , src_ns   , src_we   , src_ew   ))
        dst    = np.concatenate((dst_sn   , dst_ns   , dst_we   , dst_ew   ))
        weight = np.concatenate((weight_sn, weight_ns, weight_we, weight_ew))

        # Return graph as sparse matrix
        return sp.sparse.csr_matrix((weight, (src, dst)))
