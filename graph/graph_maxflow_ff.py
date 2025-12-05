from collections import deque


class FordFulkerson:
    def run(self, g, source, sink):
        # Lấy danh sách đỉnh
        vertices = g.get_vertices()
        n = len(vertices)

        # Map: đỉnh → index
        index_of = {v: i for i, v in enumerate(vertices)}
        node_of = {i: v for v, i in index_of.items()}

        # Tạo capacity matrix (ma trận sức chứa)
        capacity = [[0] * n for _ in range(n)]
        for u in g.adj:
            for v, w in g.adj[u].items():
                iu = index_of[u]
                iv = index_of[v]
                capacity[iu][iv] = w

        # Residual capacity
        residual = [row[:] for row in capacity]

        # BFS tìm đường tăng luồng (augmenting path)
        def bfs(s, t, parent):
            visited = [False] * n
            queue = deque([s])
            visited[s] = True
            parent[s] = -1

            while queue:
                u = queue.popleft()
                for v in range(n):
                    if not visited[v] and residual[u][v] > 0:
                        visited[v] = True
                        parent[v] = u
                        queue.append(v)

                        if v == t:
                            return True
            return False

        s = index_of[source]
        t = index_of[sink]
        parent = [-1] * n

        max_flow = 0

        # Thuật toán Edmonds–Karp
        while bfs(s, t, parent):
            # Tìm bottleneck (độ co)
            path_flow = float("inf")
            v = t
            while v != s:
                u = parent[v]
                path_flow = min(path_flow, residual[u][v])
                v = u

            # Cập nhật residual graph
            v = t
            while v != s:
                u = parent[v]
                residual[u][v] -= path_flow
                residual[v][u] += path_flow  # reverse edge
                v = u

            max_flow += path_flow

        # Trả ma trận residual như một dạng flow để debug
        return max_flow, residual


def ford_fulkerson(g, source, sink):
    return FordFulkerson().run(g, source, sink)
