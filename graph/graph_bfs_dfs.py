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
from collections import deque

def bfs(graph, start):
    """
    Duyệt BFS trên Graph.
    Trả về danh sách thứ tự duyệt.
    """
    if start not in graph.adj:
        return f"Đỉnh {start} không tồn tại trong đồ thị."

    visited = []
    seen = {start}
    queue = deque([start])

    while queue:
        u = queue.popleft()
        visited.append(u)

        for v in graph.adj[u]:
            if v not in seen:
                seen.add(v)
                queue.append(v)

    return visited




