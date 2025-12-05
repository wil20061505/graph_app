import heapq
def prim(graph, start_node=None):
    """
    Thuật toán Prim, dùng đồ thị với cấu trúc:
        graph.adj = {u: {v: weight}}
    """

    vertices = graph.get_vertices()
    if len(vertices) == 0:
        return 0, []

    if start_node is None or start_node not in vertices:
        start_node = vertices[0]

    mst_set = {start_node}
    edges_mst = []
    total_weight = 0

    pq = []

    for neighbor, w in graph.get_neighbors(start_node).items():
        heapq.heappush(pq, (w, start_node, neighbor))

    while pq and len(mst_set) < len(vertices):
        weight, u, v = heapq.heappop(pq)

        if v in mst_set:
            continue

        mst_set.add(v)
        edges_mst.append((u, v, weight))
        total_weight += weight

        for neighbor, w in graph.get_neighbors(v).items():
            if neighbor not in mst_set:
                heapq.heappush(pq, (w, v, neighbor))

    if len(mst_set) != len(vertices):
        return None, None

    return total_weight, edges_mst
