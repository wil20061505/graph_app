import heapq

def dijkstra(graph, start_node, end_node):
    """
    Dijkstra cho đồ thị:
        graph.adj = {u: {v: weight}}
    """

    vertices = graph.get_vertices()

    distances = {v: float('inf') for v in vertices}
    predecessors = {v: None for v in vertices}

    distances[start_node] = 0
    pq = [(0, start_node)]

    while pq:
        current_distance, current = heapq.heappop(pq)

        if current_distance > distances[current]:
            continue

        if current == end_node:
            break

        # neighbors là dict {v: weight}
        for neighbor, weight in graph.get_neighbors(current).items():
            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                predecessors[neighbor] = current
                heapq.heappush(pq, (new_distance, neighbor))

    if distances[end_node] == float('inf'):
        return float('inf'), None

    path = []
    node = end_node
    while node is not None:
        path.append(node)
        node = predecessors[node]

    path.reverse()
    return distances[end_node], path
