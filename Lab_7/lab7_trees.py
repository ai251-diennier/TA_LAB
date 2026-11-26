# Лабораторна робота №7. Бінарне дерево пошуку (BST) та червоно-чорне дерево (RB). Варіант 11
SEQ = [41, 52, 47, 65, 95, 38, 15, 50, 99]
RED, BLACK = "R", "B"


# ======================= Бінарне дерево пошуку =======================
class BNode:
    def __init__(self, key):
        self.key, self.left, self.right = key, None, None


def bst_insert(root, key):
    if root is None:
        return BNode(key)
    if key < root.key:
        root.left = bst_insert(root.left, key)
    elif key > root.key:
        root.right = bst_insert(root.right, key)
    return root


def bst_min(node):
    while node.left:
        node = node.left
    return node


def bst_delete(root, key, log=None):
    if root is None:
        return None
    if key < root.key:
        root.left = bst_delete(root.left, key, log)
    elif key > root.key:
        root.right = bst_delete(root.right, key, log)
    else:
        if root.left is None:
            if log is not None: log.append(f"вузол {key}: немає лівого сина -> замінюємо правим")
            return root.right
        if root.right is None:
            if log is not None: log.append(f"вузол {key}: немає правого сина -> замінюємо лівим")
            return root.left
        m = bst_min(root.right)
        if log is not None: log.append(f"вузол {key}: два сини -> ключ замінюється мінімумом правого піддерева {m.key}")
        root.key = m.key
        root.right = bst_delete(root.right, m.key)
    return root


def inorder(n, out, stack=None, depth=0):
    """Симетричний обхід; stack (якщо задано) фіксує стан стеку викликів."""
    if n is None:
        return
    if stack is not None: stack.append(("call", n.key, depth))
    inorder(n.left, out, stack, depth + 1)
    out.append(n.key)
    if stack is not None: stack.append(("visit", n.key, depth))
    inorder(n.right, out, stack, depth + 1)
    if stack is not None: stack.append(("ret", n.key, depth))


def preorder(n, out):
    if n:
        out.append(n.key); preorder(n.left, out); preorder(n.right, out)


def postorder(n, out):
    if n:
        postorder(n.left, out); postorder(n.right, out); out.append(n.key)


def bst_str(n):
    return "None" if n is None else f"{n.key}" if not (n.left or n.right) else f"{n.key}({bst_str(n.left)}, {bst_str(n.right)})"


# ======================= Червоно-чорне дерево =======================
class RNode:
    def __init__(self, key, color, nil=None):
        self.key, self.color = key, color
        self.left = self.right = self.parent = nil


class RBTree:
    def __init__(self):
        self.nil = RNode(None, BLACK)
        self.nil.left = self.nil.right = self.nil.parent = self.nil
        self.root = self.nil
        self.log = []

    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left is not self.nil: y.left.parent = x
        y.parent = x.parent
        if x.parent is self.nil: self.root = y
        elif x is x.parent.left: x.parent.left = y
        else: x.parent.right = y
        y.left = x; x.parent = y

    def rotate_right(self, x):
        y = x.left
        x.left = y.right
        if y.right is not self.nil: y.right.parent = x
        y.parent = x.parent
        if x.parent is self.nil: self.root = y
        elif x is x.parent.right: x.parent.right = y
        else: x.parent.left = y
        y.right = x; x.parent = y

    def insert(self, key):
        self.log = []
        z = RNode(key, RED, self.nil)
        y, x = self.nil, self.root
        while x is not self.nil:
            y = x
            x = x.left if key < x.key else x.right
        z.parent = y
        if y is self.nil: self.root = z
        elif key < y.key: y.left = z
        else: y.right = z
        self.log.append(f"вставлено {key} (червоний)")
        self._fix_insert(z)

    def _fix_insert(self, z):
        while z.parent.color == RED:
            p = z.parent; g = p.parent
            left = p is g.left
            u = g.right if left else g.left
            if u.color == RED:
                self.log.append(f"випадок 1: батько {p.key} і дядько {u.key} червоні -> перефарбування {p.key}, {u.key} у чорний, {g.key} у червоний")
                p.color = u.color = BLACK; g.color = RED; z = g
            else:
                if (z is p.right) == left:
                    self.log.append(f"випадок 2: дядько чорний, {z.key} – внутрішній онук -> {'лівий' if left else 'правий'} поворот навколо {p.key}")
                    z = p
                    (self.rotate_left if left else self.rotate_right)(z)
                    p = z.parent
                self.log.append(f"випадок 3: дядько чорний, {z.key} – зовнішній онук -> {p.key} чорний, {g.key} червоний, {'правий' if left else 'лівий'} поворот навколо {g.key}")
                p.color = BLACK; g.color = RED
                (self.rotate_right if left else self.rotate_left)(g)
        if self.root.color == RED:
            self.log.append(f"корінь {self.root.key} перефарбовано у чорний")
        self.root.color = BLACK

    def _transplant(self, u, v):
        if u.parent is self.nil: self.root = v
        elif u is u.parent.left: u.parent.left = v
        else: u.parent.right = v
        v.parent = u.parent

    def _min(self, x):
        while x.left is not self.nil: x = x.left
        return x

    def find(self, key):
        x = self.root
        while x is not self.nil and x.key != key:
            x = x.left if key < x.key else x.right
        return x

    def delete(self, key):
        self.log = []
        z = self.find(key)
        if z is self.nil:
            self.log.append("ключа немає"); return
        y, y_color = z, z.color
        if z.left is self.nil:
            x = z.right; self._transplant(z, z.right)
            self.log.append(f"видаляємо {key}: немає лівого сина -> замінюємо правим")
        elif z.right is self.nil:
            x = z.left; self._transplant(z, z.left)
            self.log.append(f"видаляємо {key}: немає правого сина -> замінюємо лівим")
        else:
            y = self._min(z.right); y_color = y.color; x = y.right
            self.log.append(f"видаляємо {key}: два сини -> наступник {y.key} (колір {y.color})")
            if y.parent is z: x.parent = y
            else:
                self._transplant(y, y.right); y.right = z.right; y.right.parent = y
            self._transplant(z, y); y.left = z.left; y.left.parent = y; y.color = z.color
        if y_color == BLACK:
            self.log.append("видалено чорну вершину -> порушено чорну висоту, виправлення")
            self._fix_delete(x)

    def _fix_delete(self, x):
        while x is not self.root and x.color == BLACK:
            left = x is x.parent.left
            w = x.parent.right if left else x.parent.left   # брат
            if w.color == RED:
                self.log.append(f"випадок 1: брат {w.key} червоний -> брат чорний, батько {x.parent.key} червоний, поворот навколо {x.parent.key}")
                w.color = BLACK; x.parent.color = RED
                (self.rotate_left if left else self.rotate_right)(x.parent)
                w = x.parent.right if left else x.parent.left
            near, far = (w.left, w.right) if left else (w.right, w.left)
            if near.color == BLACK and far.color == BLACK:
                self.log.append(f"випадок 2: брат {w.key} чорний, обидва його сини чорні -> брат червоний, проблема піднімається до {x.parent.key}")
                w.color = RED; x = x.parent
            else:
                if far.color == BLACK:
                    self.log.append(f"випадок 3: брат {w.key} чорний, дальній син чорний, ближній {near.key} червоний -> поворот навколо брата, перефарбування")
                    near.color = BLACK; w.color = RED
                    (self.rotate_right if left else self.rotate_left)(w)
                    w = x.parent.right if left else x.parent.left
                    near, far = (w.left, w.right) if left else (w.right, w.left)
                self.log.append(f"випадок 4: брат {w.key} чорний, дальній син {far.key} червоний -> колір брата = колір батька, батько {x.parent.key} і {far.key} чорні, поворот навколо {x.parent.key}")
                w.color = x.parent.color; x.parent.color = BLACK; far.color = BLACK
                (self.rotate_left if left else self.rotate_right)(x.parent)
                x = self.root
        if x.color == RED:
            self.log.append(f"{x.key} червоний -> фарбуємо у чорний")
        x.color = BLACK

    # допоміжні
    def inorder(self, n=None, out=None, top=True):
        if top: n, out = self.root, []
        if n is not self.nil:
            self.inorder(n.left, out, False); out.append(n.key); self.inorder(n.right, out, False)
        return out

    def preorder(self, n, out):
        if n is not self.nil:
            out.append(n.key); self.preorder(n.left, out); self.preorder(n.right, out)

    def postorder(self, n, out):
        if n is not self.nil:
            self.postorder(n.left, out); self.postorder(n.right, out); out.append(n.key)

    def black_height(self, n):
        if n is self.nil: return 1
        l, r = self.black_height(n.left), self.black_height(n.right)
        assert l == r, "порушено чорну висоту"
        return l + (n.color == BLACK)

    def check(self):
        assert self.root.color == BLACK
        def rec(n):
            if n is self.nil: return
            if n.color == RED: assert n.left.color == BLACK and n.right.color == BLACK
            rec(n.left); rec(n.right)
        rec(self.root); return self.black_height(self.root)

    def show(self, n=None, top=True):
        if top: n = self.root
        if n is self.nil: return "·"
        s = f"{n.key}{n.color}"
        return s if n.left is self.nil and n.right is self.nil else f"{s}({self.show(n.left, False)}, {self.show(n.right, False)})"


if __name__ == "__main__":
    print("=== BST: вставка ===")
    root = None
    for k in SEQ:
        root = bst_insert(root, k); print(f"+{k}: {bst_str(root)}")
    a, b, c = [], [], []
    inorder(root, a); preorder(root, b); postorder(root, c)
    print("inorder:", a); print("preorder:", b); print("postorder:", c)
    st = []; inorder(root, [], st)
    print("стан стеку викликів inorder:")
    cur = []
    for ev, k, dpt in st:
        if ev == "call": cur.append(k); print("  виклик", k, "стек:", cur)
        elif ev == "visit": print("  вивід", k)
        else: cur.pop()
    print("=== BST: видалення ===")
    for key in (root.right.key, root.left.key, root.key):
        log = []; root = bst_delete(root, key, log)
        print(f"видалення {key}:", "; ".join(log), "->", bst_str(root))
    print("=== RB: вставка ===")
    t = RBTree()
    for k in SEQ:
        t.insert(k); print(f"+{k}:", t.show(), "| bh =", t.check())
        for l in t.log: print("    ", l)
    a = t.inorder(); b = []; t.preorder(t.root, b); c = []; t.postorder(t.root, c)
    print("inorder:", a); print("preorder:", b); print("postorder:", c)
    print("=== RB: видалення чорних вершин ===")
    for key in (52, 47, 65):
        color = t.find(key).color
        t.delete(key)
        print(f"видалення {key} (колір {color}):", t.show(), "| bh =", t.check())
        for l in t.log: print("    ", l)
    a = t.inorder(); print("inorder після видалень:", a)
