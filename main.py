from pprint import pprint

ITEMS = {
    'r': (3, 25),  # винтовка
    'p': (2, 15),  # пистолет
    'a': (2, 15),  # боекомплект
    'm': (2, 20),  # аптечка
    'i': (1, 5),   # ингалятор
    'k': (1, 15),  # нож
    'x': (3, 20),  # топор
    't': (1, 25),  # оберег
    'f': (1, 15),  # фляжка
    'd': (1, 10),  # антидот
    's': (2, 20),  # еда
    'c': (2, 20),  # арбалет
}

INITIAL_POINTS = 20 
REQUIRED = {'d'}


def solve_knapsack(max_cells: int):
    # считаем обяз. предметов
    req_weight = sum(ITEMS[k][0] for k in REQUIRED)
    req_points = sum(ITEMS[k][1] for k in REQUIRED)

    if req_weight > max_cells:
        print("Обязательный предмет не влезают в рюкзак.")
        return

    capacity = max_cells - req_weight
    base_points = INITIAL_POINTS + req_points

    # список ост. предметов
    free_items = [k for k in ITEMS.keys() if k not in REQUIRED]
    n = len(free_items)

    # макс. очков от первых i предметов при вместимости w
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        key = free_items[i - 1]
        w_i,p_i  = ITEMS[key]
        for w in range(1, capacity + 1):
            # не берём
            best = dp[i - 1][w]
            # возьмем
            if w_i <= w:
                cand = p_i + dp[i - 1][w - w_i]
                if cand > best:
                    best = cand
            dp[i][w] = best

    # набор вещей
    w = capacity
    chosen_list = []
    i = n
    while i > 0 and w > 0:
        if dp[i][w] == dp[i - 1][w]:
            i -= 1  # не взяли
        else:
            key = free_items[i - 1]
            chosen_list.append(key)
            w -= ITEMS[key][0]
            i -= 1

    # добавляем обязательные (антидот 'd')
    chosen_list.extend(REQUIRED)

    total_points = base_points + dp[n][capacity]

    # превращаем предметы в список ячеек
    cells = []
    for key in chosen_list:     
        w_i, _ = ITEMS[key]
        cells.extend([key] * w_i)

    rows, cols = 2, 4
    grid = [['   ' for _ in range(cols)] for _ in range(rows)]

    for idx, key in enumerate(cells):
        if idx >= rows * cols:
            break
        r = idx // cols
        c = idx % cols
        grid[r][c] = f'[{key}]'

    for row in grid:
        print(','.join(row))

    print(f"\nИтоговые очки выживания: {total_points}")


if __name__ == "__main__":
    # 8 ячеек
    solve_knapsack(8)
    # 7 ячеек
    solve_knapsack(7)
