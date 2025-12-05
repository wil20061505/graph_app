import numpy as np

def to_adjacency_matrix(graph):
    nodes = sorted(graph.get_vertices())
    index = {node: i for i, node in enumerate(nodes)}
    n = len(nodes)

    M = np.zeros((n, n), dtype=int)

    for u in graph.adj:
        for v, w in graph.adj[u].items():
            M[index[u]][index[v]] = w

    return nodes, M
