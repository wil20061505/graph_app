def bfs(graph, start):
    if start not in graph.adj:
        return f"Đỉnh {start} không tồn tại trong đồ thị."

    visited = []
    queue = [start]
    seen = set([start])

    while queue:
        u = queue.pop(0)
        visited.append(u)

        # neighbors: dict {v: weight}
        for v in graph.adj[u].keys():
            if v not in seen:
                seen.add(v)
                queue.append(v)

    return visited


def dfs(graph, start):
    if start not in graph.adj:
        return f"Đỉnh {start} không tồn tại trong đồ thị."

    visited = []
    stack = [start]
    seen = set()

    while stack:
        u = stack.pop()

        if u not in seen:
            seen.add(u)
            visited.append(u)

            # reversed để giữ thứ tự giống list cũ
            for v in reversed(list(graph.adj[u].keys())):
                if v not in seen:
                    stack.append(v)

    return visited
