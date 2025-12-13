import collections

def ford_fulkerson(graph, source, sink, record_steps=False):
    """
    Ford–Fulkerson với BFS (Edmonds–Karp)
    Trả về: (max_flow, steps)
    steps chỉ có nếu record_steps=True
    """

    # Tạo residual graph dạng {u: {v: cap}}
    residual = {}
    for u in graph.adj:
        residual.setdefault(u, {})
        for v, w in graph.adj[u].items():
            residual[u][v] = w
            residual.setdefault(v, {})
            if u not in residual[v]:
                residual[v][u] = 0

    steps = []
    max_flow = 0

    # ---------------- BFS tìm đường tăng ----------------
    def bfs():
        parent = {source: None}
        queue = collections.deque([source])

        while queue:
            u = queue.popleft()
            for v, cap in residual[u].items():
                if cap > 0 and v not in parent:
                    parent[v] = u
                    if v == sink:
                        return parent
                    queue.append(v)
        return None

    # ---------------- Lặp tới khi hết đường tăng ----------------
    while True:
        parent = bfs()
        if parent is None:
            break

        # reconstruct path
        path = []
        v = sink
        while v != source:
            u = parent[v]
            path.append((u, v))
            v = u
        path.reverse()

        # bottleneck
        bottleneck = min(residual[u][v] for u, v in path)

        # update residual
        for u, v in path:
            residual[u][v] -= bottleneck
            residual[v][u] += bottleneck

        max_flow += bottleneck

        if record_steps:
            # deep copy residual
            res_copy = {u: dict(vs) for u, vs in residual.items()}
            steps.append({
                "augment_path": path.copy(),
                "bottleneck": bottleneck,
                "flow_added": max_flow,
                "residual": res_copy
            })

    return (max_flow, steps) if record_steps else max_flow
