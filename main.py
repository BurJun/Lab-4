from itertools import combinations

# --- Константы варианта ---
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
    'd': (1, 10),  # антидот (обязателен при заражении)
    's': (2, 20),  # еда
    'c': (2, 20),  # арбалет
}

W = 4
H = 2                # инвентарь 2x4
MAX_CELLS = W * H          
INITIAL_POINTS = 20
MIN_POINTS = 0
REQUIRED_ITEMS = {'d'}     # болезнь: заражение

# --- Логика подбора ---
def weight(items): return sum(ITEMS[k][0] for k in items)
def points(items): return INITIAL_POINTS + sum(ITEMS[k][1] for k in items)

def is_valid(items) -> bool:
    return (
        weight(items) <= MAX_CELLS and
        points(items) > MIN_POINTS and
        REQUIRED_ITEMS.issubset(items)
    )

def all_valid_combinations():
    keys = list(ITEMS.keys())
    best = None  # (combo, pts)
    valid = []
    for r in range(1, len(keys) + 1):
        for combo in combinations(keys, r):
            if is_valid(combo):
                pts = points(combo)
                valid.append((combo, pts))
                if best is None or pts > best[1]:
                    best = (combo, pts)
    return valid, best

# --- Укладка в инвентарь 2x4 ---
def pack_inventory(combo, w=W, h=H):
    grid = [[' ' for _ in range(w)] for _ in range(h)]
    for item in combo:
        size = ITEMS[item][0]
        placed = False
        for i in range(h):
            j = 0
            while j < w:
                if j + size <= w and all(grid[i][j+s] == ' ' for s in range(size)):
                    for s in range(size):
                        grid[i][j+s] = item
                    placed = True
                    break
                j += 1
            if placed: break
        # если не влезло подряд в строку — пропускаем (простая укладка)
    return grid

def save_result(filename, combo, pts, grid):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("Лучшая комбинация:\n")
        f.write(f"Items: {list(combo)}, Survival points: {pts}\n\n")
        f.write(f"Инвентарь {H}x{W}:\n")
        for row in grid:
            f.write(f"[{' ] [ '.join(row)}]\n")

def main():
    valid, best = all_valid_combinations()
    if not best:
        print("Нет валидных комбинаций при заданных ограничениях.")
        return
    combo, pts = best
    grid = pack_inventory(combo)
    save_result("validCombinations.txt", combo, pts, grid)
    print("Готово: validCombinations.txt")

if __name__ == "__main__":
    main()
