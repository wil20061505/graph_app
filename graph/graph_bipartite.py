from collections import deque

def is_bipartite(graph):
    """
    Kiểm tra đồ thị hai phía.
    Đồ thị dùng cấu trúc: graph.adj = {u: {v: weight}}.
    Dùng BFS + tô màu 2 màu.
    """

    vertices = graph.get_vertices()
    if not vertices:
        return True

    # 0: chưa tô màu, 1 và -1 là hai màu khác nhau
    colors = {v: 0 for v in vertices}

    for start in vertices:
        if colors[start] != 0:
            continue

        colors[start] = 1
        queue = deque([start])

        while queue:
            u = queue.popleft()

            # Duyệt neighbors dạng {neighbor: weight}
            for v in graph.get_neighbors(u).keys():

                if colors[v] == 0:  
                    colors[v] = -colors[u]
                    queue.append(v)

                elif colors[v] == colors[u]:
                    return False

    return True
