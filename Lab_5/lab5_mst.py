# Лабораторна робота №5. Мінімальне кістякове дерево: алгоритми Пріма та Крускала. Варіант 11
INF = float("inf")
N = 8  # вершини 1..8
# Ребра графа варіанту 11: (u, v, вага)
EDGES = [(1, 3, 1), (1, 2, 4), (1, 4, 4), (3, 8, 4), (3, 6, 5), (3, 4, 5),
         (2, 6, 3), (2, 5, 7), (6, 7, 6), (8, 7, 5), (4, 5, 1), (5, 7, 4)]


def adjacency_matrix(n=N, edges=EDGES):
    g = [[INF] * n for _ in range(n)]
    for u, v, w in edges:
        g[u - 1][v - 1] = w
        g[v - 1][u - 1] = w
    return g


def adjacency_lists(n=N, edges=EDGES):
    adj = {v: [] for v in range(1, n + 1)}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    for v in adj:
        adj[v].sort()
    return adj


def prim(g, start=0, trace=False):
    """Алгоритм Пріма (матриця суміжності). Повертає (ребра MST, вага)."""
    n = len(g)
    selected = [False] * n
    selected[start] = True
    mst, total = [], 0
    for step in range(1, n):
        best = INF
        x = y = -1
        for i in range(n):
            if selected[i]:
                for j in range(n):
                    if not selected[j] and g[i][j] < best:  # ребро (i, j) існує і j ще не в дереві
                        best, x, y = g[i][j], i, j
        if trace:
            cand = [(i + 1, j + 1, g[i][j]) for i in range(n) if selected[i]
                    for j in range(n) if not selected[j] and g[i][j] < INF]
            print(f"Крок {step}: V_T={sorted(k + 1 for k in range(n) if selected[k])}")
            print("  допустимі ребра:", ", ".join(f"({a},{b})={w}" for a, b, w in cand))
            print(f"  e* = ({x + 1},{y + 1}) = {best}")
        selected[y] = True
        mst.append((x + 1, y + 1, best))
        total += best
    return mst, total


class DSU:
    def __init__(self, n):
        self.parent = list(range(n + 1))

    def find(self, i):
        while self.parent[i] != i:
            self.parent[i] = self.parent[self.parent[i]]
            i = self.parent[i]
        return i

    def union(self, u, v):
        self.parent[self.find(u)] = self.find(v)


def kruskal(n=N, edges=EDGES, trace=False):
    """Алгоритм Крускала (сортування ребер + DSU). Повертає (ребра MST, вага)."""
    order = sorted(edges, key=lambda e: (e[2], e[0], e[1]))
    dsu = DSU(n)
    mst, total = [], 0
    if trace:
        print("Відсортовані ребра:", ", ".join(f"({u},{v})={w}" for u, v, w in order))
    for u, v, w in order:
        if dsu.find(u) != dsu.find(v):
            dsu.union(u, v)
            mst.append((u, v, w))
            total += w
            if trace:
                print(f"Беремо ({u},{v})={w}: FIND({u}) != FIND({v}) -> додаємо, |E_T|={len(mst)}")
        elif trace:
            print(f"Пропускаємо ({u},{v})={w}: утворюється цикл")
        if len(mst) == n - 1:
            break
    return mst, total


if __name__ == "__main__":
    g = adjacency_matrix()
    print("Матриця суміжності (0 - немає ребра):")
    for i, row in enumerate(g, 1):
        print(i, [0 if x == INF else x for x in row])
    print("Списки суміжності:")
    for v, lst in adjacency_lists().items():
        print(v, "->", lst)
    print("\n--- Алгоритм Пріма (старт: вершина 1) ---")
    m1, w1 = prim(g, 0, trace=True)
    print("MST:", ", ".join(f"({u},{v})={w}" for u, v, w in m1), "| вага =", w1)
    print("\n--- Алгоритм Крускала ---")
    m2, w2 = kruskal(trace=True)
    print("MST:", ", ".join(f"({u},{v})={w}" for u, v, w in m2), "| вага =", w2)
    same = {frozenset((u, v)) for u, v, _ in m1} == {frozenset((u, v)) for u, v, _ in m2}
    print("Однакові множини ребер:", same)
