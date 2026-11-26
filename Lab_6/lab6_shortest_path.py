# Лабораторна робота №6. Найкоротші шляхи: алгоритми Дейкстри та Флойда. Варіант 11
import heapq
INF = float("inf")
N = 8  # вершини 1..8
EDGES = [(1, 3, 1), (1, 2, 4), (1, 4, 4), (3, 8, 4), (3, 6, 5), (3, 4, 5),
         (2, 6, 3), (2, 5, 7), (6, 7, 6), (8, 7, 5), (4, 5, 1), (5, 7, 4)]


def adjacency_lists(n=N, edges=EDGES):
    adj = {v: [] for v in range(1, n + 1)}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    for v in adj:
        adj[v].sort()
    return adj


def adjacency_matrix(n=N, edges=EDGES):
    g = [[INF] * n for _ in range(n)]
    for i in range(n):
        g[i][i] = 0
    for u, v, w in edges:
        g[u - 1][v - 1] = g[v - 1][u - 1] = w
    return g


def dijkstra(adj, s, trace=False):
    """Алгоритм Дейкстри з чергою з пріоритетом. Повертає (dist, pred)."""
    dist = {v: INF for v in adj}
    pred = {v: None for v in adj}
    dist[s] = 0
    done = set()
    pq = [(0, s)]
    step = 0
    while pq:
        d, u = heapq.heappop(pq)
        if u in done:           # застарілий запис черги
            continue
        done.add(u)
        step += 1
        changed = []
        for v, w in adj[u]:
            if v not in done and d + w < dist[v]:
                dist[v] = d + w
                pred[v] = u
                heapq.heappush(pq, (dist[v], v))
                changed.append(f"{v}: {d}+{w}={d + w}")
        if trace:
            print(f"Крок {step}: обрано {u} (dist={d}); оновлено: {', '.join(changed) or '—'}")
            print("   dist =", [("∞" if dist[v] == INF else dist[v]) for v in sorted(dist)],
                  " pred =", [pred[v] or "-" for v in sorted(pred)])
    return dist, pred


def path_to(pred, s, t):
    p = []
    while t is not None:
        p.append(t)
        t = pred[t]
    return p[::-1] if p[-1] == s else []


def floyd(g, trace=False):
    """Алгоритм Флойда–Уоршелла. Повертає (D, P, історію матриць D(k))."""
    n = len(g)
    D = [row[:] for row in g]
    P = [[(i if (i != j and g[i][j] < INF) else None) for j in range(n)] for i in range(n)]  # предок j на шляху з i
    hist = [([r[:] for r in D], [])]
    for k in range(n):
        ch = []
        for i in range(n):
            for j in range(n):
                if D[i][k] + D[k][j] < D[i][j]:
                    ch.append((i + 1, j + 1, D[i][j], D[i][k], D[k][j]))
                    D[i][j] = D[i][k] + D[k][j]
                    P[i][j] = P[k][j]
        hist.append(([r[:] for r in D], ch))
        if trace:
            print(f"D({k + 1}): змінено елементів {len(ch)}")
            for i, j, old, a, b in ch:
                if i < j:
                    print(f"   d[{i}][{j}] = min({'∞' if old == INF else old}, d[{i}][{k + 1}]+d[{k + 1}][{j}] = {a}+{b}) = {a + b}")
    return D, P, hist


def floyd_path(P, i, j):
    if P[i][j] is None and i != j:
        return []
    p = [j]
    while j != i:
        j = P[i][j]
        p.append(j)
    return [x + 1 for x in p[::-1]]


if __name__ == "__main__":
    adj = adjacency_lists()
    print("--- Алгоритм Дейкстри (старт: вершина 1) ---")
    dist, pred = dijkstra(adj, 1, trace=True)
    for v in sorted(dist):
        print(f"1 -> {v}: вага {dist[v]}, шлях {' - '.join(map(str, path_to(pred, 1, v)))}")
    print("\n--- Алгоритм Флойда ---")
    D, P, hist = floyd(adjacency_matrix(), trace=True)
    print("Підсумкова матриця D(8):")
    for i, row in enumerate(D, 1):
        print(i, row)
    print("Рядок 1 Флойда збігається з Дейкстрою:", [D[0][v - 1] for v in sorted(dist)] == [dist[v] for v in sorted(dist)])
    print("Шляхи Флойда з вершини 1:", {v: floyd_path(P, 0, v - 1) for v in range(2, N + 1)})
