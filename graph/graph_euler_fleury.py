import copy

def bfs_count_reachable_nodes(input_graph, input_start_node):
    """
    Hàm phụ trợ: Đếm số lượng đỉnh có thể đi tới từ đỉnh bắt đầu.
    Dùng để kiểm tra tính chất Cầu (Bridge).
    """
    if input_start_node not in input_graph.adj:
        return 0
        
    visited_nodes = {input_start_node}
    queue_nodes = [input_start_node]
    count_nodes = 1 # Đếm cả đỉnh bắt đầu

    while queue_nodes:
        current_processing_node = queue_nodes.pop(0)
        
        # Duyệt qua các đỉnh kề
        for neighbor_node_info in input_graph.adj.get(current_processing_node, []):
            # neighbor_node_info có thể là tuple (node, weight) hoặc chỉ node
            # Xử lý để lấy node id
            neighbor_id = neighbor_node_info[0] if isinstance(neighbor_node_info, (list, tuple)) else neighbor_node_info
            
            if neighbor_id not in visited_nodes:
                visited_nodes.add(neighbor_id)
                queue_nodes.append(neighbor_id)
                count_nodes += 1
                
    return count_nodes

def fleury(input_graph):
    """
    Thuật toán Fleury tìm đường đi/chu trình Euler.
    """
    # Tạo bản sao để không làm hỏng dữ liệu gốc
    # Tên biến mô tả rõ ý nghĩa: working_graph (đồ thị đang làm việc)
    working_graph = copy.deepcopy(input_graph)
    
    # 1. Kiểm tra điều kiện Euler và tìm đỉnh bắt đầu
    # Lấy danh sách các đỉnh có bậc lẻ
    list_odd_degree_nodes = []
    for node_id, neighbors_list in working_graph.adj.items():
        if len(neighbors_list) % 2 != 0:
            list_odd_degree_nodes.append(node_id)
            
    # Điều kiện: 0 đỉnh lẻ (Chu trình) hoặc 2 đỉnh lẻ (Đường đi)
    if len(list_odd_degree_nodes) not in [0, 2]:
        return "Không tồn tại đường đi hay chu trình Euler."

    # Chọn đỉnh bắt đầu: Nếu có đỉnh lẻ thì bắt đầu từ đó, không thì bắt đầu từ đỉnh bất kỳ (ví dụ đỉnh đầu tiên trong dict)
    current_node = list_odd_degree_nodes[0] if list_odd_degree_nodes else next(iter(working_graph.adj))
    
    # Biến đầu ra
    output_euler_path = [current_node]

    # Hàm kiểm tra xem cạnh nối (u, v) có hợp lệ để đi không
    def is_valid_edge(check_u, check_v):
        # 1. Nếu v là đỉnh kề duy nhất của u, bắt buộc phải đi
        if len(working_graph.adj[check_u]) == 1:
            return True
        
        # 2. Kiểm tra xem cạnh (check_u, check_v) có phải là Cầu (Bridge) không
        # a. Đếm số đỉnh đến được trước khi xóa cạnh
        count_before_remove = bfs_count_reachable_nodes(working_graph, check_u)
        
        # b. Xóa tạm cạnh
        working_graph.remove_edge(check_u, check_v)
        
        # c. Đếm số đỉnh đến được sau khi xóa
        count_after_remove = bfs_count_reachable_nodes(working_graph, check_u)
        
        # d. Thêm lại cạnh (hoàn tác) để xét tiếp hoặc chọn đi thật
        working_graph.add_edge(check_u, check_v, 1) # Giả sử trọng số 1 hoặc lấy từ dữ liệu cũ nếu cần
        
        # Nếu số lượng đỉnh đến được giảm -> Là Cầu -> Không nên đi (trừ khi là duy nhất)
        return count_before_remove <= count_after_remove

    # Vòng lặp chính: Chạy khi đỉnh hiện tại vẫn còn cạnh nối
    while working_graph.adj.get(current_node):
        found_next_step = False
        
        # Lấy danh sách các hàng xóm (copy ra list mới để tránh lỗi khi sửa đổi trong loop)
        neighbors_data = list(working_graph.adj[current_node])
        
        for neighbor_info in neighbors_data:
            target_neighbor = neighbor_info[0] if isinstance(neighbor_info, (list, tuple)) else neighbor_info
            
            if is_valid_edge(current_node, target_neighbor):
                # Nếu cạnh hợp lệ, thực hiện di chuyển
                output_euler_path.append(target_neighbor)
                working_graph.remove_edge(current_node, target_neighbor)
                current_node = target_neighbor
                found_next_step = True
                break
        
        # Nếu duyệt hết hàng xóm mà không đi được (trường hợp hiếm do đồ thị không liên thông), dừng lại
        if not found_next_step:
            break
            
    return output_euler_path