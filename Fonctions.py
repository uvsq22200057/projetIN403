def connexe(v):
    pass


def shortest(d, a):
    pass


def create_table():
    pass


def pp(graph, node, visited):
    visited[node] = True
    for neighbor in graph[node]:
        if not visited[neighbor]:
            pp(graph, neighbor, visited)


def connexe_pp(graph):
    n = len(graph)
    visited = [False] * n
    pp(graph, 0, visited)  # On commence le parcours depuis un nœud arbitraire
    return all(visited)