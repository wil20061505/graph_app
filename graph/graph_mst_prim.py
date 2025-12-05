import heapq

class Graph:
    """Định nghĩa lớp Đồ thị cơ bản cho thuật toán Prim (vô hướng, có trọng số)."""
    def __init__(self):
        # Đồ thị được lưu trữ dưới dạng: {đỉnh_u: {đỉnh_v: trọng_số_uv, ...}, ...}
        self.adj = {}

    def add_vertex(self, u):
        """Thêm một đỉnh nếu nó chưa tồn tại."""
        if u not in self.adj:
            self.adj[u] = {}

    def add_edge(self, u, v, weight):
        """Thêm cạnh vô hướng có trọng số giữa u và v."""
        self.add_vertex(u)
        self.add_vertex(v)
        
        # Thêm cạnh cho cả hai chiều (vô hướng)
        self.adj[u][v] = int(weight)
        self.adj[v][u] = int(weight)

    def get_vertices(self):
        """Trả về danh sách tất cả các đỉnh trong đồ thị."""
        return list(self.adj.keys())

def prim(graph, start_node=None):
    """
    Tìm Cây Bao Trùm Tối Thiểu (MST) bằng thuật toán Prim.
    
    Args:
        graph (Graph): Đối tượng đồ thị.
        start_node (str, optional): Đỉnh bắt đầu. Mặc định là đỉnh đầu tiên nếu không có.
        
    Returns:
        tuple: (tổng_trọng_số_mst, danh_sách_cạnh_của_mst)
    """
    vertices = graph.get_vertices()
    if not vertices:
        return 0, []

    # 1. Khởi tạo
    if start_node is None or start_node not in vertices:
        start_node = vertices[0] # Chọn đỉnh đầu tiên làm đỉnh bắt đầu nếu không được chỉ định
    
    # mst_set: Tập hợp các đỉnh đã nằm trong MST
    mst_set = {start_node}
    
    # edges_in_mst: Danh sách các cạnh tạo nên MST
    edges_in_mst = []
    
    # priority_queue (hàng đợi ưu tiên): (trọng_số, đỉnh_đang_xét, đỉnh_kề)
    # Ta chỉ cần lưu (trọng_số, đỉnh_kề) từ đỉnh_đang_xét
    pq = []
    
    # Đưa tất cả các cạnh của đỉnh bắt đầu vào hàng đợi ưu tiên
    for neighbor, weight in graph.adj.get(start_node, {}).items():
        # (weight, neighbor, start_node) -> (trọng số, đỉnh_mới, đỉnh_trong_mst)
        heapq.heappush(pq, (weight, neighbor, start_node))

    total_weight = 0

    # 2. Vòng lặp chính
    # Lặp cho đến khi tất cả các đỉnh đều nằm trong MST
    while pq and len(mst_set) < len(vertices):
        # Lấy cạnh có trọng số nhỏ nhất (cạnh nhẹ nhất)
        weight, v, u = heapq.heappop(pq)
        
        # Kiểm tra tính hợp lệ: Nếu đỉnh v (đỉnh mới) đã nằm trong MST, bỏ qua
        if v in mst_set:
            continue
            
        # 3. Thêm đỉnh v và cạnh (u, v) vào MST
        mst_set.add(v)
        edges_in_mst.append((u, v, weight))
        total_weight += weight
        
        # 4. Cập nhật các cạnh kề mới từ đỉnh v
        for neighbor, new_weight in graph.adj.get(v, {}).items():
            # Nếu đỉnh kề chưa nằm trong MST, đưa cạnh mới vào hàng đợi
            if neighbor not in mst_set:
                # (new_weight, neighbor, v) -> (trọng số, đỉnh_mới, đỉnh_trong_mst)
                heapq.heappush(pq, (new_weight, neighbor, v))

    # Kiểm tra xem có phải là cây bao trùm hay không (đồ thị phải liên thông)
    if len(mst_set) == len(vertices):
        return total_weight, edges_in_mst
    else:
        # Đồ thị không liên thông, không có MST
        return None, None 

