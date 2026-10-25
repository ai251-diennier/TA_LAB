# Лабораторна робота №1. Сортування вибором. Варіант 11


def selection_sort(arr, trace=False):
    n = len(arr)
    comparisons = 0
    assignments = 0
    if trace:
        print("Початковий масив:", arr)
        print("-" * 30)
    # Зовнішній цикл: від 0 до n-2 (n-1 проходів)
    for i in range(n - 1):
        # Припускаємо, що поточний елемент є мінімальним
        min_index = i
        assignments += 1
        if trace:
            print(f"Ітерація {i}:")
            print(f"Поточний елемент (для обміну): arr[{i}] = {arr[i]}")
            print(f"Шукаємо мінімальний елемент у частині: {arr[i:]}")
        # Внутрішній цикл шукає найменший елемент в решті списку
        for j in range(i + 1, n):
            comparisons += 1
            if arr[j] < arr[min_index]:
                min_index = j
                assignments += 1
        if trace:
            print(f"Знайдено мінімальний елемент: arr[{min_index}] = {arr[min_index]}")
        # Обмін елементів, якщо знайдено новий мінімальний
        comparisons += 1
        if min_index != i:
            if trace:
                print(f"Обмін arr[{i}] ({arr[i]}) і arr[{min_index}] ({arr[min_index]})")
            arr[i], arr[min_index] = arr[min_index], arr[i]
            assignments += 3
        elif trace:
            print("Обмін не потрібен")
        if trace:
            print(f"Масив після ітерації {i}: {arr}")
            print("-" * 30)
    if trace:
        print("Сортування завершено.")
        print("Фінальний відсортований масив:", arr)
        print("Загальна кількість порівнянь:", comparisons)
        print("Загальна кількість присвоєнь:", assignments)
    return arr, comparisons, assignments


if __name__ == "__main__":
    my_list = [47, 50, 61, 41, 53, 12, 68, 63, 3]  # варіант 11
    sorted_list, comps, assigs = selection_sort(my_list.copy())
    print("Оригінальний список:", my_list)
    print("Відсортований список:", sorted_list)
    print(f"Кількість порівнянь: {comps}")
    print(f"Кількість присвоєнь: {assigs}")
    print()
    selection_sort(my_list.copy(), trace=True)
