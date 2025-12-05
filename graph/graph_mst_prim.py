def prim(graph, start_node=None):
    vertices = graph.get_vertices()
    if not vertices:
        return 0, []

    if start_node is None:
        start_node = vertices[0]

    mst_set = {start_node}
    edges = []
    pq = []

    import heapq

    for v, w in graph.adj[start_node].items():
        heapq.heappush(pq, (w, start_node, v))

    total = 0

    while pq and len(mst_set) < len(vertices):
        w, u, v = heapq.heappop(pq)

        if v in mst_set:
            continue

        mst_set.add(v)
        edges.append((u, v, w))
        total += w

        for nv, nw in graph.adj[v].items():
            if nv not in mst_set:
                heapq.heappush(pq, (nw, v, nv))

    if len(mst_set) != len(vertices):
        return None, None

    return total, edges
