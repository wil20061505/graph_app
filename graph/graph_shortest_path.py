import heapq # Cần thư viện heapq (priority queue) để tối ưu thuật toán Dijkstra

class Graph:
    """Định nghĩa lớp Đồ thị cơ bản sử dụng Dictionary (Adjacency List)."""
    def __init__(self):
        # Đồ thị được lưu trữ dưới dạng: {đỉnh_u: {đỉnh_v: trọng_số_uv, ...}, ...}
        self.adj = {}

    def add_edge(self, u, v, weight):
        """Thêm cạnh có hướng từ u đến v với trọng số."""
        # Đảm bảo đỉnh u và v tồn tại trong đồ thị
        if u not in self.adj:
            self.adj[u] = {}
        if v not in self.adj:
            self.adj[v] = {}
            
        # Thêm cạnh
        self.adj[u][v] = int(weight) # Đảm bảo trọng số là số nguyên

    def get_vertices(self):
        """Trả về danh sách tất cả các đỉnh trong đồ thị."""
        return list(self.adj.keys())

def dijkstra(graph, start_node, end_node):
    """
    Tìm đường đi ngắn nhất từ start_node đến end_node bằng thuật toán Dijkstra.
    
    Args:
        graph (Graph): Đối tượng đồ thị.
        start_node (str): Đỉnh bắt đầu.
        end_node (str): Đỉnh kết thúc.
        
    Returns:
        tuple: (khoảng_cách_ngắn_nhất, đường_đi_là_danh_sách_các_đỉnh) 
               hoặc (float('inf'), None) nếu không tìm thấy đường đi.
    """
    
    # 1. Khởi tạo
    # distances: Lưu trữ khoảng cách ngắn nhất hiện tại từ start_node đến mỗi đỉnh.
    distances = {vertex: float('inf') for vertex in graph.get_vertices()}
    distances[start_node] = 0
    
    # predecessors: Lưu trữ đỉnh tiền nhiệm (đỉnh đứng trước) trên đường đi ngắn nhất.
    predecessors = {vertex: None for vertex in graph.get_vertices()}
    
    # priority_queue (hàng đợi ưu tiên): (khoảng_cách, đỉnh)
    pq = [(0, start_node)]
    
    # 2. Vòng lặp chính của thuật toán
    while pq:
        # Lấy đỉnh có khoảng cách ngắn nhất hiện tại
        current_distance, current_node = heapq.heappop(pq)
        
        # Nếu khoảng cách đã lấy ra lớn hơn khoảng cách đã ghi nhận, bỏ qua (đã có đường đi tốt hơn)
        if current_distance > distances[current_node]:
            continue
            
        # Nếu đã đến đích, dừng lại
        if current_node == end_node:
            break
            
        # 3. Duyệt qua các đỉnh kề
        # graph.adj.get(current_node, {}) đảm bảo không bị lỗi nếu đỉnh không có cạnh kề
        for neighbor, weight in graph.adj.get(current_node, {}).items():
            distance = current_distance + weight
            
            # Thư giãn (Relaxation): Nếu tìm thấy đường đi ngắn hơn
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    # 4. Xây dựng đường đi (Path Reconstruction)
    shortest_distance = distances[end_node]
    
    if shortest_distance == float('inf'):
        # Không tìm thấy đường đi
        return float('inf'), None
    
    # Xây dựng đường đi ngược từ đích về nguồn
    path = []
    current = end_node
    while current is not None:
        path.append(current)
        current = predecessors[current]
        
    path.reverse() # Đảo ngược để có đường đi từ start_node đến end_node
    
    return shortest_distance, path
