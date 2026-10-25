# Лабораторна робота №2. Швидке сортування за схемою Хоара. Варіант 11


def partition(a, l, r, trace=False, pad=""):
    """Розбиття за схемою Хоара. Повертає (q, comparisons, assignments)."""
    comparisons = 0
    assignments = 0
    pivot = a[l]
    assignments += 1
    i = l - 1
    j = r + 1
    assignments += 2
    if trace:
        print(f"{pad}Вибираємо опорний елемент (pivot): {pivot}")
    while True:
        # Шукаємо елемент, що більший або рівний опорному
        i += 1
        assignments += 1
        while a[i] < pivot:
            comparisons += 1
            i += 1
            assignments += 1
        comparisons += 1  # порівняння, на якому цикл завершився
        # Шукаємо елемент, що менший або рівний опорному
        j -= 1
        assignments += 1
        while a[j] > pivot:
            comparisons += 1
            j -= 1
            assignments += 1
        comparisons += 1  # порівняння, на якому цикл завершився
        comparisons += 1  # порівняння i >= j
        if trace:
            print(f"{pad}Поточні індекси: i = {i}, j = {j}.", end=" ")
        if i >= j:
            if trace:
                print(f"Масив: {a[l:r + 1]}")
                print(f"{pad}Індекси перетнулися. Поділ завершено. Повертаємо j={j}.")
            return j, comparisons, assignments
        if trace:
            print(f"Обмінюємо a[{i}] ({a[i]}) і a[{j}] ({a[j]}).", end=" ")
        a[i], a[j] = a[j], a[i]
        assignments += 3
        if trace:
            print(f"Масив: {a[l:r + 1]}")


def quicksort(a, l, r, trace=False, depth=0):
    """Повертає (comparisons, assignments, recursive_calls); кожен виклик (включно з тривіальними) рахується."""
    pad = "  " * depth
    comparisons = 0
    assignments = 0
    recursive_calls = 1
    if trace:
        print(f"{pad}Quicksort виклик: масив = {a}, l = {l}, r = {r}")
    if l < r:
        q, c1, a1 = partition(a, l, r, trace, pad)
        comparisons += c1
        assignments += a1
        # Рекурсивні виклики для лівого та правого підмасивів
        c2, a2, r2 = quicksort(a, l, q, trace, depth + 1)
        c3, a3, r3 = quicksort(a, q + 1, r, trace, depth + 1)
        comparisons += c2 + c3
        assignments += a2 + a3
        recursive_calls += r2 + r3
        if trace:
            print(f"{pad}Після Quicksort для l={l}, r={r}: масив = {a}")
    return comparisons, assignments, recursive_calls


if __name__ == "__main__":
    my_list = [47, 50, 61, 41, 53, 12, 68, 63, 3]  # варіант 11
    original_list = my_list.copy()
    print("Оригінальний список:", original_list)
    total_c, total_a, total_calls = quicksort(my_list, 0, len(my_list) - 1)
    print("Відсортований список:", my_list)
    print(f"Загальна кількість порівнянь: {total_c}")
    print(f"Загальна кількість присвоювань: {total_a}")
    print(f"Загальна кількість рекурсивних викликів: {total_calls}")
    print()
    print("--- Quicksort за схемою Хоара з трасуванням ---")
    my_list = original_list.copy()
    quicksort(my_list, 0, len(my_list) - 1, trace=True)
