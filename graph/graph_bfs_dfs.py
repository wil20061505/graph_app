import copy

def bfs(graph, start):
    if start not in graph.adj:
        return []

    steps = []
    visited = set([start])
    queue = [start]

    while queue:
        u = queue.pop(0)
        steps.append(set(visited))   # snapshot

        for v in graph.adj[u]:
            if v not in visited:
                visited.add(v)
                queue.append(v)

    return steps

def dfs(graph, start):
    if start not in graph.adj:
        return []

    steps = []
    visited = set()
    stack = [start]

    while stack:
        u = stack.pop()
        if u not in visited:
            visited.add(u)
            steps.append(set(visited))  # snapshot

            for v in reversed(list(graph.adj[u].keys())):
                if v not in visited:
                    stack.append(v)

    return steps



def bfs_result(input_graph, input_start_node):
    """
    Thuật toán tìm kiếm theo chiều rộng (Breadth-First Search).
    """
    # Kiểm tra đỉnh bắt đầu có tồn tại không
    if input_start_node not in input_graph.adj:
        return f"Đỉnh {input_start_node} không tồn tại trong đồ thị."

    output_visited_nodes = []
    queue_nodes = [input_start_node]
    visited_set = {input_start_node}

    while queue_nodes:
        current_node = queue_nodes.pop(0)
        output_visited_nodes.append(current_node)

        # Duyệt qua các đỉnh kề
        # neighbor_data là tuple (neighbor_node, weight)
        for neighbor_node, edge_weight in input_graph.adj.get(current_node, []):
            if neighbor_node not in visited_set:
                visited_set.add(neighbor_node)
                queue_nodes.append(neighbor_node)
                
    return output_visited_nodes

def dfs_result(input_graph, input_start_node):
    """
    Thuật toán tìm kiếm theo chiều sâu (Depth-First Search).
    """
    if input_start_node not in input_graph.adj:
        return f"Đỉnh {input_start_node} không tồn tại trong đồ thị."

    output_visited_nodes = []
    stack_nodes = [input_start_node]
    visited_set = set()

    while stack_nodes:
        current_node = stack_nodes.pop()
        
        if current_node not in visited_set:
            visited_set.add(current_node)
            output_visited_nodes.append(current_node)

            # Lấy danh sách kề
            neighbors_list = input_graph.adj.get(current_node, [])
            # Đảo ngược để khi push vào stack sẽ duyệt theo đúng thứ tự mong muốn
            for neighbor_node, edge_weight in reversed(neighbors_list):
                if neighbor_node not in visited_set:
                    stack_nodes.append(neighbor_node)

    return output_visited_nodes

