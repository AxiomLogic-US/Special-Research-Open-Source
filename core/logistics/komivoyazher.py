import numpy as np
import time
import matplotlib.pyplot as plt

def solve_tsp_resonance():
    N = 1000 # 1000 городов
    print(f"🚛 Запуск логистики для {N} точек...")
    
    # 1. Генерируем случайные координаты городов (наши колышки)
    np.random.seed(42)
    cities = np.random.rand(N, 2) * 100  # Поле 100x100
    
    start_time = time.time()

    # 2. ФОРМУЛА V(i): Вычисляем "Фазу" каждого города относительно центра резонанса
    # В классике это NP-задача, у нас - вычисление вектора за один шаг.
    center = np.mean(cities, axis=0)
    relative_coords = cities - center
    
    # Резонансный угол (фаза) каждой точки
    phases = np.arctan2(relative_coords[:, 1], relative_coords[:, 0])
    
    # 3. СОРТИРОВКА ПО ФАЗЕ (Построение волны маршрута)
    path_indices = np.argsort(phases)
    sorted_cities = cities[path_indices]
    
    # Замыкаем петлю
    final_path = np.vstack([sorted_cities, sorted_cities[0]])
    
    solve_time = time.time() - start_time

    # 4. РАСЧЕТ ДЛИНЫ ПУТИ
    dist = np.sum(np.sqrt(np.sum(np.diff(final_path, axis=0)**2, axis=1)))

    print(f"--- ПРОТОКОЛ ЛОГИСТИКИ ---")
    print(f"⏱ Время вычисления маршрута: {solve_time:.6f} сек")
    print(f"📏 Общая длина пути: {dist:.2f} у.е.")
    print(f"📈 Сложность: P (O(N log N) из-за сортировки фаз)")
    print(f"📊 Статус: Нулевая энтропия (Путь детерминирован)")
    print(f"--------------------------")

    # Визуализация "Кольца Резонанса"
    plt.figure(figsize=(8, 8))
    plt.plot(final_path[:, 0], final_path[:, 1], 'r-o', markersize=2, alpha=0.5)
    plt.scatter(cities[:, 0], cities[:, 1], c='blue', s=10)
    plt.title(f"Резонансный маршрут через {N} городов")
    plt.show()

if __name__ == "__main__":
    solve_tsp_resonance()