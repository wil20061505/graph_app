import copy

def hierholzer(input_graph):
    """
    Thuật toán Hierholzer tìm đường đi/chu trình Euler.
    """
    # Tạo bản sao đồ thị
    working_graph = copy.deepcopy(input_graph)

    # 1. Kiểm tra điều kiện và tìm đỉnh bắt đầu
    list_odd_degree_nodes = []
    
    # Đếm bậc các đỉnh
    # Nếu đồ thị có hướng cần tính bán bậc ra/vào (out_degree, in_degree) riêng
    for node_id, neighbors_list in working_graph.adj.items():
        if len(neighbors_list) % 2 != 0:
            list_odd_degree_nodes.append(node_id)
    
    if len(list_odd_degree_nodes) not in [0, 2]:
         return "Không tồn tại đường đi hay chu trình Euler."

    # Chọn đỉnh bắt đầu
    start_execution_node = list_odd_degree_nodes[0] if list_odd_degree_nodes else next(iter(working_graph.adj))

    # Khởi tạo các biến lưu trữ
    # processing_stack: Stack dùng để duyệt thám hiểm (DFS style)
    processing_stack = [start_execution_node] 
    
    # output_euler_circuit: Danh sách chứa kết quả đường đi
    output_euler_circuit = []

    # Vòng lặp xử lý Stack
    while processing_stack:
        # Lấy đỉnh ở trên cùng stack (nhưng chưa lấy ra hẳn - peek)
        current_vertex = processing_stack[-1]

        # Kiểm tra xem đỉnh này còn cạnh nào nối đi nơi khác không
        if working_graph.adj.get(current_vertex):
            # Lấy đỉnh kề đầu tiên trong danh sách kề
            neighbor_info = working_graph.adj[current_vertex][0]
            target_neighbor = neighbor_info[0] if isinstance(neighbor_info, (list, tuple)) else neighbor_info
            
            # Đẩy đỉnh kề vào stack để duyệt tiếp
            processing_stack.append(target_neighbor)
            
            # Xóa cạnh vừa đi qua để không đi lại ("đốt cầu")
            working_graph.remove_edge(current_vertex, target_neighbor)
        else:
            # Nếu đỉnh hiện tại không còn đường đi (ngõ cụt trong lượt duyệt này)
            # Lấy nó ra khỏi stack và thêm vào kết quả cuối cùng
            finished_vertex = processing_stack.pop()
            output_euler_circuit.append(finished_vertex)

    # Kết quả của Hierholzer được thêm vào theo thứ tự ngược, nên cần đảo ngược lại list
    output_euler_circuit.reverse()
    
    return output_euler_circuit