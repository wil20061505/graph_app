import copy

def hierholzer(graph):
    """
    Thuật toán Hierholzer tìm chu trình hoặc đường đi Euler.
    Áp dụng cho đồ thị vô hướng dùng cấu trúc:
        adj[u] = {v: weight, ...}
    """
    # Sao chép để giữ nguyên đồ thị gốc
    g = copy.deepcopy(graph)

    # --- 1. Kiểm tra bậc các đỉnh ---
    odd_nodes = [u for u in g.adj if len(g.adj[u]) % 2 == 1]

    if len(odd_nodes) not in (0, 2):
        return "Không tồn tại đường đi hay chu trình Euler."

    # Nếu có 2 đỉnh lẻ → đó là điểm đầu
    start = odd_nodes[0] if odd_nodes else next(iter(g.adj))

    # Stack duyệt thuật toán
    stack = [start]
    path = []

    # --- 2. Hierholzer ---
    while stack:
        u = stack[-1]

        # Nếu còn cạnh
        if g.adj[u]:
            # Lấy một hàng xóm bất kỳ
            v = next(iter(g.adj[u].keys()))

            # Đi sang v
            stack.append(v)

            # Xóa cạnh u–v
            g.remove_edge(u, v)

        else:
            # Ngõ cụt → đưa vào kết quả
            path.append(stack.pop())

    # Đảo chiều path vì thuật toán sinh ra ngược
    path.reverse()

    return path
