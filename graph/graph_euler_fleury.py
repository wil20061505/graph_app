import copy

def bfs_count_reachable_nodes(graph, start):
    """
    Đếm số đỉnh có thể đi tới từ 1 đỉnh.
    Dùng để kiểm tra cạnh có phải cầu hay không.
    """
    if start not in graph.adj:
        return 0

    visited = {start}
    queue = [start]

    while queue:
        u = queue.pop(0)
        for v in graph.adj[u].keys():   # v là node kề
            if v not in visited:
                visited.add(v)
                queue.append(v)

    return len(visited)


def fleury(graph):
    """
    Thuật toán Fleury tìm đường đi hoặc chu trình Euler.
    Áp dụng cho đồ thị vô hướng.
    """
    # Sao chép để không làm hỏng dữ liệu gốc
    g = copy.deepcopy(graph)

    # --- 1. Tìm các đỉnh bậc lẻ ---
    odd_nodes = [u for u in g.adj if len(g.adj[u]) % 2 == 1]

    # Điều kiện Euler
    if len(odd_nodes) not in (0, 2):
        return "Không tồn tại đường đi hay chu trình Euler."

    # Đỉnh bắt đầu
    current = odd_nodes[0] if odd_nodes else next(iter(g.adj))

    path = [current]

    def is_valid_edge(u, v):
        """
        Kiểm tra cạnh (u, v) có phải cầu hay không.
        """
        # 1. Nếu chỉ có 1 cạnh để đi → phải đi
        if len(g.adj[u]) == 1:
            return True

        # 2. Đếm số đỉnh reachable trước khi xóa
        c1 = bfs_count_reachable_nodes(g, u)

        # 3. Xóa cạnh (u, v)
        g.remove_edge(u, v)

        # 4. Đếm lại
        c2 = bfs_count_reachable_nodes(g, u)

        # 5. Thêm lại cạnh
        #    Lấy đúng trọng số cũ
        g.add_edge(u, v, graph.adj[u][v], undirected=True)

        # Nếu giảm → đó là cầu → không được đi
        return c1 <= c2

    # --- 2. Duyệt Fleury ---
    while g.adj.get(current):
        for v in list(g.adj[current].keys()):
            if is_valid_edge(current, v):
                # Đi cạnh này
                path.append(v)
                g.remove_edge(current, v)
                current = v
                break

    return path
