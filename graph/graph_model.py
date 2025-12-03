class Graph:
    def __init__(self):
        # Lưu danh sách kề (Adjacency List)
        # Cấu trúc: {tên_đỉnh: [(đỉnh_kề, trọng_số), ...]}
        self.adj = {}

    def add_edge(self, input_source_node, input_target_node, input_weight=1):
        """
        Thêm cạnh từ đỉnh nguồn (source) đến đỉnh đích (target) với trọng số (weight).
        """
        # Đảm bảo các đỉnh tồn tại trong danh sách kề
        if input_source_node not in self.adj:
            self.adj[input_source_node] = []
        if input_target_node not in self.adj:
            self.adj[input_target_node] = []
        
        # Thêm cạnh vào danh sách kề
        # Lưu dưới dạng tuple: (neighbor, weight)
        self.adj[input_source_node].append((input_target_node, int(input_weight)))