import networkx as nx
import matplotlib.pyplot as plt

def draw_graph_with_highlight(graph, visited_nodes):
    """
    Vẽ graph và tô màu các đỉnh đã duyệt
    """
    G = nx.Graph()

    for u in graph.adj:
        G.add_node(u)

    for u in graph.adj:
        for v, w in graph.adj[u].items():
            G.add_edge(u, v, weight=w)

    pos = nx.spring_layout(G, seed=42)

    node_colors = [
        "orange" if node in visited_nodes else "lightgray"
        for node in G.nodes()
    ]

    fig, ax = plt.subplots()
    nx.draw(G, pos, with_labels=True, node_color=node_colors, ax=ax)
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

    return fig
