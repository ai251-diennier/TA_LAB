# Лабораторна робота №4. Хеш-таблиці: хешування з ланцюжками та з відкритою адресацією. Варіант 11
import math

PROVERB = "Не той багатий, у кого багато грошей, а той, у кого душа багата"
A_CONST = 0.6180339887  # константа Кнута (метод множення)
M_DIV = 13   # розмір таблиці для методу ділення
M_MUL = 16   # розмір таблиці для методу множення

ALPHABET = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
LETTER_POSITIONS = {ch: i + 1 for i, ch in enumerate(ALPHABET)}


def get_words(text):
    """Слова прислів'я (нижній регістр, без розділових знаків), кожне слово один раз у порядку першої появи."""
    words = [w.strip(",.;:!?—-").lower() for w in text.split()]
    unique = []
    for w in words:
        if w and w not in unique:
            unique.append(w)
    return unique


def key_value(word):
    """Числовий ключ k = сума номерів позицій букв українського алфавіту."""
    return sum(LETTER_POSITIONS.get(ch, 0) for ch in word)


def hash_division(word, m=M_DIV):
    """Метод ділення: h(k) = k mod m."""
    return key_value(word) % m


def hash_multiplication(word, m=M_MUL, a=A_CONST):
    """Метод множення: h(k) = floor(m * (k*A mod 1))."""
    k = key_value(word)
    return math.floor(m * ((k * a) % 1))


# ---------------- Відкрите хешування (ланцюжки) ----------------
def build_open_hash_table(words, m, hash_func):
    table = [[] for _ in range(m)]
    for word in words:
        table[hash_func(word, m)].append(word)
    return table


def display_open_table(table, title):
    print(f"\n--- {title} ---")
    for i, chain in enumerate(table):
        print(f"Індекс {i:02d}: {chain}")


def search_open(table, word, hash_func):
    """Повертає (знайдено, кількість порівнянь)."""
    comparisons = 0
    for item in table[hash_func(word, len(table))]:
        comparisons += 1
        if item == word:
            return True, comparisons
    return False, comparisons


# ---------------- Закрите хешування (відкрита адресація, лінійне дослідження) ----------------
def build_closed_hash_table(words, m, hash_func):
    table = [None] * m
    steps = []
    for word in words:
        start = hash_func(word, m)
        for i in range(m):
            address = (start + i) % m
            if table[address] is None:
                table[address] = word
                steps.append((word, start, i + 1, address))
                break
        else:
            print(f"Помилка: таблиця заповнена. Не вдалося додати слово: {word}")
    return table, steps


def display_closed_table(table, title):
    print(f"\n--- {title} ---")
    print("Індекс | Слово")
    print("-------|-------")
    for i, item in enumerate(table):
        print(f"{i:02d} | {item if item is not None else '(NULL)'}")


def search_closed(table, word, hash_func):
    """Повертає (знайдено, кількість порівнянь/досліджених комірок)."""
    m = len(table)
    start = hash_func(word, m)
    probes = 0
    for i in range(m):
        address = (start + i) % m
        if table[address] is None:
            return False, probes
        probes += 1
        if table[address] == word:
            return True, probes
    return False, probes


if __name__ == "__main__":
    words = get_words(PROVERB)
    print("Слова:", words)
    for w in words:
        print(f"{w:10s} k={key_value(w):3d}  ділення: {hash_division(w)}  множення: {hash_multiplication(w)}")
    for name, hf, m in (("ділення", hash_division, M_DIV), ("множення", hash_multiplication, M_MUL)):
        t = build_open_hash_table(words, m, hf)
        display_open_table(t, f"Хешування з ланцюжками, метод {name} (M={m})")
        cmp_ = {w: search_open(t, w, hf)[1] for w in words}
        print("Порівнянь на пошук:", cmp_, "середнє =", sum(cmp_.values()) / len(cmp_))
        t, steps = build_closed_hash_table(words, m, hf)
        display_closed_table(t, f"Відкрита адресація, метод {name} (M={m})")
        cmp_ = {w: search_closed(t, w, hf)[1] for w in words}
        print("Порівнянь на пошук:", cmp_, "середнє =", sum(cmp_.values()) / len(cmp_))
