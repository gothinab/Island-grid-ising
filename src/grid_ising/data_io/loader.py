import networkx as nx
import numpy as np
from numba.typed import List


class NetworkFaultTolerance:
    def __init__(self, network_graph):
        self.network_graph = network_graph

        self.nodes = list(self.network_graph.nodes())
        self.num_nodes = len(self.nodes)
        self.num_edges = self.network_graph.number_of_edges()

        adj_matrix = nx.to_scipy_sparse_array(
            self.network_graph,
            nodelist=self.nodes,
            weight='weight',
            format='csr',
        )

        self.neighbors_indices = List()
        self.neighbors_weights = List()

        for i in range(self.num_nodes):
            start, end = adj_matrix.indptr[i], adj_matrix.indptr[i + 1]
            self.neighbors_indices.append(adj_matrix.indices[start:end].astype(np.int64))
            self.neighbors_weights.append(adj_matrix.data[start:end].astype(np.float64))

    @property
    def mean_degree(self):
        return 2.0 * self.num_edges / self.num_nodes