import numpy as np

def to_adjacency_matrix(input_graph):
    """
    Chuyển đổi từ danh sách kề sang ma trận kề.
    """
    # Lấy danh sách tất cả các đỉnh và sắp xếp
    output_node_labels = sorted(input_graph.adj.keys())
    
    # Tạo map ánh xạ tên đỉnh sang index (ví dụ: 'A' -> 0, 'B' -> 1)
    node_to_index_map = {node_name: index for index, node_name in enumerate(output_node_labels)}
    number_of_nodes = len(output_node_labels)
    
    # Khởi tạo ma trận toàn số 0 kích thước n x n
    output_adjacency_matrix = np.zeros((number_of_nodes, number_of_nodes), dtype=int)
    
    # Duyệt qua từng đỉnh và cập nhật trọng số vào ma trận
    for source_node in input_graph.adj:
        for target_node, edge_weight in input_graph.adj[source_node]:
            row_index = node_to_index_map[source_node]
            col_index = node_to_index_map[target_node]
            output_adjacency_matrix[row_index][col_index] = edge_weight
            
    return output_node_labels, output_adjacency_matrix