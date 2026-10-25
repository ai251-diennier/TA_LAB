# Лабораторна робота №3. Сортування купою (Heapsort). Варіант 11


def swap(arr, i, j):
    """Міняє місцями два елементи в масиві."""
    arr[i], arr[j] = arr[j], arr[i]


def sink(arr, i, n, stats, trace=False):
    """Занурення елемента arr[i] у купі розміром n.
    stats = [comparisons, assignments] накопичується."""
    k = i
    stats[1] += 1
    if trace:
        print(f"Починаємо 'занурювати' елемент: {arr[i]} з індексу {i}")
    while True:
        j = 2 * k + 1  # індекс лівого дочірнього елемента
        stats[1] += 1
        if j >= n:
            if trace:
                print(f" Елемент {arr[k]} на індексі {k} досяг кінця купи. Завершуємо.")
            break
        # Знаходимо індекс найбільшого дочірнього елемента
        if j + 1 < n:
            stats[0] += 1
            if trace:
                print(f" Порівнюємо {arr[j]} (лівий) та {arr[j + 1]} (правий). Обираємо {max(arr[j], arr[j + 1])}")
            if arr[j + 1] > arr[j]:
                j += 1
                stats[1] += 1
        elif trace:
            print(f" Обираємо лівий дочірній елемент: {arr[j]} на індексі {j}")
        # Порівнюємо поточний елемент з найбільшим дочірнім
        stats[0] += 1
        if arr[k] >= arr[j]:
            if trace:
                print(f" {arr[k]} (батько) >= {arr[j]} (найбільший дочірній). Елемент на своєму місці.")
            break
        if trace:
            print(f" Міняємо місцями {arr[k]} (батько) та {arr[j]} (дочірній)")
        swap(arr, k, j)
        stats[1] += 3
        k = j
        stats[1] += 1
        if trace:
            print(f" Масив після обміну: {arr}")


def heapsort(arr, verbose=False, trace=False):
    """Пірамідальне сортування. Повертає (arr, comparisons, assignments)."""
    n = len(arr)
    stats = [0, 0]  # [comparisons, assignments]
    stats[1] += 1  # n = len(arr)
    if verbose:
        print(f"Початковий масив: {arr}\n")
        print("--- Фаза 1: Побудова максимальної купи ---")
    # Фаза 1: побудова максимальної купи
    for i in range(n // 2 - 1, -1, -1):
        if verbose:
            print(f"Занурюємо елемент з індексу {i}: {arr[i]}")
        sink(arr, i, n, stats, trace)
        if trace:
            print("-" * 30)
    if verbose:
        print(f"\nМасив після побудови купи: {arr}\n")
        print("--- Фаза 2: Сортування ---")
    # Фаза 2: сортування
    for i in range(n - 1, 0, -1):
        if verbose:
            print(f"Міняємо місцями корінь ({arr[0]}) та останній елемент ({arr[i]})")
        swap(arr, 0, i)
        stats[1] += 3
        n -= 1
        stats[1] += 1
        if verbose:
            print(f"Розмір купи зменшився до {n}. Відновлюємо властивості купи.")
        sink(arr, 0, n, stats, trace)
        if verbose:
            print(f"Масив на поточному кроці: {arr}\n")
    return arr, stats[0], stats[1]


if __name__ == "__main__":
    A = [47, 50, 61, 41, 53, 12, 68, 63, 3]  # варіант 11
    sorted_A, comps, assigs = heapsort(A.copy(), verbose=True)
    print(f"Відсортований масив: {sorted_A}")
    print(f"Кількість порівнянь: {comps}")
    print(f"Кількість присвоювань: {assigs}")
    print()
    print("--- Детальне трасування ---")
    heapsort(A.copy(), trace=True)
