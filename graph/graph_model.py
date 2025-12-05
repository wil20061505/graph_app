class Graph:
    """
    Đồ thị vô hướng hoặc có hướng, có trọng số.
    Lưu bằng cấu trúc chuẩn:
        adj = {
            u: {v: weight_uv, ...},
            ...
        }
    Dùng chung cho:
    """
    def __init__(self):
        self.adj = {}

    def add_vertex(self, node):
        """
        Thêm một đỉnh nếu chưa tồn tại.
        """
        if node not in self.adj:
            self.adj[node] = {}

    def add_edge(self, source, target, weight=1, undirected=False):
        """
        Thêm cạnh từ source → target với trọng số weight.
        Nếu undirected=True thì thêm luôn cả chiều ngược lại.
        """
        self.add_vertex(source)
        self.add_vertex(target)

        w = int(weight)
        self.adj[source][target] = w

        if undirected:
            self.adj[target][source] = w

    def get_vertices(self):
        """
        Trả về danh sách tất cả các đỉnh.
        """
        return list(self.adj.keys())

    def get_neighbors(self, node):
        """
        Trả về dict các đỉnh kề dạng:
           {neighbor: weight}
        """
        return self.adj.get(node, {})

    def __repr__(self):
        """
        Hiển thị ngắn gọn đồ thị.
        """
        return f"Graph(adj={self.adj})"
