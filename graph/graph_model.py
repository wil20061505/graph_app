class Graph:
    """
    Đồ thị vô hướng hoặc có hướng, có trọng số.
    Lưu bằng cấu trúc:
        adj = {
            u: {v: weight_uv, ...},
            ...
        }
    """
    def __init__(self):
        self.adj = {}

    def add_vertex(self, node):
        if node not in self.adj:
            self.adj[node] = {}

    def add_edge(self, source, target, weight=1, undirected=False):
        """
        Thêm cạnh source → target.
        Nếu undirected=True thì thêm cả target → source.
        """
        self.add_vertex(source)
        self.add_vertex(target)

        w = int(weight)
        self.adj[source][target] = w

        if undirected:
            self.adj[target][source] = w

    def has_edge(self, u, v):
        """
        Kiểm tra tồn tại cạnh u → v.
        """
        return u in self.adj and v in self.adj[u]

    def remove_edge(self, u, v, undirected=False):
        """
        Xóa cạnh u → v.
        Nếu undirected=True, xóa luôn v → u.
        """
        if u in self.adj and v in self.adj[u]:
            del self.adj[u][v]

        if undirected and v in self.adj and u in self.adj[v]:
            del self.adj[v][u]

    def get_vertices(self):
        return list(self.adj.keys())

    def get_neighbors(self, node):
        """
        Trả về dict {neighbor: weight}
        """
        return self.adj.get(node, {})

    def degree(self, node):
        """
        Bậc của đỉnh trong đồ thị vô hướng.
        """
        return len(self.adj.get(node, {}))

    def __repr__(self):
        return f"Graph(adj={self.adj})"
