import copy

def bfs(graph, start):
    if start not in graph.adj:
        return []

    steps = []
    visited = set([start])
    queue = [start]

    while queue:
        u = queue.pop(0)
        steps.append(set(visited))   # snapshot

        for v in graph.adj[u]:
            if v not in visited:
                visited.add(v)
                queue.append(v)

    return steps

def dfs(graph, start):
    if start not in graph.adj:
        return []

    steps = []
    visited = set()
    stack = [start]

    while stack:
        u = stack.pop()
        if u not in visited:
            visited.add(u)
            steps.append(set(visited))  # snapshot

            for v in reversed(list(graph.adj[u].keys())):
                if v not in visited:
                    stack.append(v)

    return steps





