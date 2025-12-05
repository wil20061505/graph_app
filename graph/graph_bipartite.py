from collections import deque

class Graph:
    """Định nghĩa lớp Đồ thị cơ bản sử dụng Dictionary (Adjacency List)."""
    def __init__(self):
        # Đồ thị được lưu trữ dưới dạng: {đỉnh_u: [đỉnh_kề_v1, đỉnh_kề_v2, ...], ...}
        self.adj = {}
    
    def add_vertex(self, u):
        """Thêm một đỉnh nếu nó chưa tồn tại."""
        if u not in self.adj:
            self.adj[u] = []

    def add_edge(self, u, v):
        """Thêm cạnh vô hướng giữa u và v."""
        self.add_vertex(u)
        self.add_vertex(v)
        # Thêm cạnh cho cả hai chiều (đồ thị vô hướng)
        self.adj[u].append(v)
        self.adj[v].append(u)

    def get_vertices(self):
        """Trả về danh sách tất cả các đỉnh trong đồ thị."""
        return list(self.adj.keys())

def is_bipartite(graph):
    """
    Kiểm tra đồ thị có phải là đồ thị hai phía hay không bằng phương pháp tô màu 2 màu (BFS).
    
    Args:
        graph (Graph): Đối tượng đồ thị.
        
    Returns:
        bool: True nếu đồ thị là hai phía, False nếu không.
    """
    
    vertices = graph.get_vertices()
    if not vertices:
        return True  # Đồ thị rỗng được coi là hai phía

    # colors: Dictionary để lưu trữ màu của các đỉnh. 0: chưa tô màu, 1: Màu 1, -1: Màu 2
    colors = {v: 0 for v in vertices}
    
    # Duyệt qua tất cả các đỉnh (để xử lý các đồ thị có nhiều thành phần liên thông)
    for start_node in vertices:
        if colors[start_node] == 0:
            # Bắt đầu BFS từ thành phần liên thông này
            queue = deque([start_node])
            colors[start_node] = 1  # Tô màu đỉnh bắt đầu là Màu 1
            
            while queue:
                u = queue.popleft()
                
                # Duyệt qua các đỉnh kề của u
                for v in graph.adj.get(u, []):
                    if colors[v] == 0:
                        # Nếu v chưa được tô màu, tô màu ngược lại với u và đưa v vào hàng đợi
                        colors[v] = -colors[u]
                        queue.append(v)
                        
                    elif colors[v] == colors[u]:
                        # Nếu v và u (đỉnh kề) có cùng màu, đồ thị KHÔNG phải là hai phía
                        return False

    return True # Nếu duyệt xong mà không có xung đột màu, đồ thị là hai phía

