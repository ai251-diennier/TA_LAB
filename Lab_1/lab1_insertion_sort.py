# Лабораторна робота №1. Сортування вставками. Варіант 11


def insertion_sort(arr, trace=False):
    n = len(arr)
    comparisons = 0
    assignments = 0
    if trace:
        print("Початковий масив:", arr)
        print("-" * 30)
    # i - індекс елемента, який потрібно вставити
    for i in range(1, n):
        key = arr[i]
        assignments += 1
        j = i - 1
        assignments += 1
        if trace:
            print(f"Ітерація {i}:")
            print(f"Елемент для вставки (key): {key}")
            print(f"Відсортована частина: {arr[:i]}")
        # Зсуваємо елементи, що більші за key, вправо
        while j >= 0 and arr[j] > key:
            comparisons += 1
            if trace:
                print(f"Порівняння: {arr[j]} > {key}. True. Зсуваємо {arr[j]} вправо.")
            arr[j + 1] = arr[j]
            assignments += 1
            j -= 1
            assignments += 1
        # Додаткове порівняння, коли умова while стає false
        if j >= 0:
            comparisons += 1
            if trace:
                print(f"Порівняння: {arr[j]} > {key}. False. Цикл завершено.")
        elif trace:
            print("Досягнуто початку масиву. Цикл завершено.")
        arr[j + 1] = key
        assignments += 1
        if trace:
            print(f"Вставка {key} на позицію {j + 1}.")
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
    sorted_list, comps, assigs = insertion_sort(my_list.copy())
    print("Оригінальний список:", my_list)
    print("Відсортований список:", sorted_list)
    print(f"Кількість порівнянь: {comps}")
    print(f"Кількість присвоєнь: {assigs}")
    print()
    insertion_sort(my_list.copy(), trace=True)
