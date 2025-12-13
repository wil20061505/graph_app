import copy

def dfs(graph, start):
    """
    Duyệt DFS trên Graph.
    Trả về danh sách thứ tự duyệt.
    """
    if start not in graph.adj:
        return f"Đỉnh {start} không tồn tại trong đồ thị."

    visited = []
    seen = set()
    stack = [start]

    while stack:
        u = stack.pop()

        if u not in seen:
            seen.add(u)
            visited.append(u)

            # duyệt theo thứ tự adj (đảo để giống đệ quy)
            for v in reversed(list(graph.adj[u].keys())):
                if v not in seen:
                    stack.append(v)

    return visited

def bfs(graph, start):
    """
    Đếm số đỉnh reachable từ start (BFS).
    Dùng để kiểm tra cạnh có phải là cầu hay không.
    """
    if start not in graph.adj:
        return 0

    visited = {start}
    queue = [start]

    while queue:
        u = queue.pop(0)
        for v in graph.adj[u]:
            if v not in visited:
                visited.add(v)
                queue.append(v)

    return len(visited)


def fleury(graph):
    """
    Thuật toán Fleury tìm đường đi / chu trình Euler
    Áp dụng cho đồ thị vô hướng
    """
    # copy graph để không phá dữ liệu gốc
    g = copy.deepcopy(graph)

    # 1. tìm các đỉnh bậc lẻ
    odd_nodes = [u for u in g.adj if len(g.adj[u]) % 2 == 1]

    # điều kiện Euler
    if len(odd_nodes) not in (0, 2):
        return "Không tồn tại đường đi hay chu trình Euler."

    # chọn đỉnh bắt đầu
    current = odd_nodes[0] if odd_nodes else next(iter(g.adj))
    path = [current]

    def is_valid_edge(u, v):
        """
        Kiểm tra cạnh (u, v) có phải là cạnh hợp lệ để đi hay không
        (không phải cầu, trừ khi bắt buộc)
        """
        # nếu chỉ còn 1 cạnh thì buộc phải đi
        if len(g.adj[u]) == 1:
            return True

        # số đỉnh reachable trước khi xóa
        c1 = bfs(g, u)

        # lưu trọng số
        weight = g.adj[u][v]

        # xóa cạnh (vô hướng)
        g.remove_edge(u, v, undirected=True)

        # số đỉnh reachable sau khi xóa
        c2 = bfs(g, u)

        # thêm lại cạnh
        g.add_edge(u, v, weight, undirected=True)

        # nếu không làm giảm số đỉnh reachable → KHÔNG phải cầu
        return c2 == c1

    # 2. duyệt Fleury
    while g.adj[current]:
        for v in list(g.adj[current].keys()):
            if is_valid_edge(current, v):
                path.append(v)
                g.remove_edge(current, v, undirected=True)
                current = v
                break

    return path
