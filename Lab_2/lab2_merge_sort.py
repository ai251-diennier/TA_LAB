# Лабораторна робота №2. Сортування злиттям (ітеративне та рекурсивне). Варіант 11


# ---------------- Ітеративна версія ----------------
def merge(a, left, mid, right, trace=False):
    comparisons = 0
    assignments = 0
    n1 = mid - left
    n2 = right - mid
    # Створюємо тимчасові підмасиви
    L = a[left:mid]
    R = a[mid:right]
    assignments += n1 + n2
    if trace:
        print(f"Об'єднуємо підмасиви: a[{left}:{mid}] ({L}) і a[{mid}:{right}] ({R})")
    it1 = 0
    it2 = 0
    k = left
    assignments += 3  # присвоєння it1, it2, k
    # Зливаємо елементи, порівнюючи їх
    while it1 < n1 and it2 < n2:
        comparisons += 1
        if trace:
            print(f"Порівняння: {L[it1]} <= {R[it2]}")
        if L[it1] <= R[it2]:  # <= забезпечує стійкість
            a[k] = L[it1]
            it1 += 1
        else:
            a[k] = R[it2]
            it2 += 1
        assignments += 1
        k += 1
        assignments += 1
    # Копіюємо елементи, що залишилися з першого підмасиву
    while it1 < n1:
        a[k] = L[it1]
        it1 += 1
        k += 1
        assignments += 1
    # Копіюємо елементи, що залишилися з другого підмасиву
    while it2 < n2:
        a[k] = R[it2]
        it2 += 1
        k += 1
        assignments += 1
    if trace:
        print(f"Масив після об'єднання: {a}")
        print("-" * 30)
    return comparisons, assignments


def merge_sort_iterative(a, trace=False):
    n = len(a)
    comparisons = 0
    assignments = 0
    if trace:
        print("Початковий масив:", a)
        print("-" * 30)
    i = 1
    while i < n:
        j = 0
        while j < n - i:
            left = j
            mid = j + i
            right = min(j + 2 * i, n)
            c, a_count = merge(a, left, mid, right, trace)
            comparisons += c
            assignments += a_count
            j += 2 * i
        i *= 2
    return a, comparisons, assignments


# ---------------- Рекурсивна версія ----------------
def merge_lists(left, right, trace=False, pad=""):
    merged_arr = []
    comparisons = 0
    assignments = 0
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        comparisons += 1
        if left[i] <= right[j]:
            if trace:
                print(f"{pad}Порівняння: {left[i]} <= {right[j]} -> True. Додаємо {left[i]}")
            merged_arr.append(left[i])
            i += 1
        else:
            if trace:
                print(f"{pad}Порівняння: {left[i]} <= {right[j]} -> False. Додаємо {right[j]}")
            merged_arr.append(right[j])
            j += 1
        assignments += 1
    while i < len(left):
        if trace:
            print(f"{pad}Додаємо залишок з лівого масиву: {left[i]}")
        merged_arr.append(left[i])
        i += 1
        assignments += 1
    while j < len(right):
        if trace:
            print(f"{pad}Додаємо залишок з правого масиву: {right[j]}")
        merged_arr.append(right[j])
        j += 1
        assignments += 1
    if trace:
        print(f"{pad}Злиття завершено. Результат: {merged_arr}")
    return merged_arr, comparisons, assignments


def merge_sort_recursive(arr, trace=False, depth=0):
    """Повертає (відсортований список, порівняння, присвоєння, рекурсивні виклики)."""
    pad = "  " * depth
    comparisons = 0
    assignments = 0
    recursive_calls = 1  # цей виклик
    if trace:
        print(f"{pad}Розділяємо масив: {arr}")
    if len(arr) <= 1:
        return arr, comparisons, assignments, recursive_calls
    mid = len(arr) // 2
    assignments += 1
    left_half, c1, a1, r1 = merge_sort_recursive(arr[:mid], trace, depth + 1)
    right_half, c2, a2, r2 = merge_sort_recursive(arr[mid:], trace, depth + 1)
    comparisons += c1 + c2
    assignments += a1 + a2
    recursive_calls += r1 + r2
    if trace:
        print(f"{pad}Зливаємо {left_half} та {right_half}")
    merged_arr, c_merge, a_merge = merge_lists(left_half, right_half, trace, pad)
    comparisons += c_merge
    assignments += a_merge
    return merged_arr, comparisons, assignments, recursive_calls


if __name__ == "__main__":
    my_list = [47, 50, 61, 41, 53, 12, 68, 63, 3]  # варіант 11
    print("--- ІТЕРАТИВНА ВЕРСІЯ ---")
    print("Оригінальний список:", my_list)
    sorted_list, comps, assigs = merge_sort_iterative(my_list.copy())
    print("Відсортований список:", sorted_list)
    print(f"Кількість порівнянь: {comps}")
    print(f"Кількість присвоювань: {assigs}")
    print()
    print("--- РЕКУРСИВНА ВЕРСІЯ ---")
    print("Оригінальний список:", my_list)
    sorted_list, comps, assigs, calls = merge_sort_recursive(my_list)
    print("Відсортований список:", sorted_list)
    print(f"Загальна кількість порівнянь: {comps}")
    print(f"Загальна кількість присвоювань: {assigs}")
    print(f"Загальна кількість рекурсивних викликів: {calls}")
