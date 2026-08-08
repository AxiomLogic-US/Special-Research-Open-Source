import torch
import numpy as np
import matplotlib.pyplot as plt

class ElementPurifierPro:
    def __init__(self, raw_particles=200000):
        self.n = raw_particles
        self.phi_gold = (1 + 5**0.5) / 2 # Шаг "Нити"
        
    def get_element_signature(self, element_name):
        # Реальные физические параметры (упрощенно для модели)
        signatures = {
            "Gold": {"omega": 79.197, "color": "gold"},
            "Silver": {"omega": 47.107, "color": "silver"},
            "Copper": {"omega": 29.635, "color": "#B87333"}
        }
        return signatures.get(element_name, {"omega": 1.0, "color": "blue"})

    def separate(self, element_name, purity_target=0.999):
        sig = self.get_element_signature(element_name)
        omega = sig["omega"]
        
        print(f"🌀 Настройка сепаратора на {element_name} (Omega: {omega})")
        
        # Создаем поток "грязных" индексов
        indices = torch.arange(self.n, dtype=torch.float32)
        
        # ФОРМУЛА: Резонанс P_valid
        # Мы ищем точки, где фаза волны элемента совпадает с шагом пространства
        phase = (indices * self.phi_gold) % (2 * np.pi)
        resonance = torch.cos(phase - (omega % (2 * np.pi)))
        
        # Фильтр чистоты 99.9%
        mask = resonance > purity_target
        captured = torch.sum(mask).item()
        
        # Формируем КРИСТАЛЛИЧЕСКУЮ РЕШЕТКУ (не цилиндр, а структуру)
        # Располагаем атомы по спирали Ферма для максимальной плотности
        k = torch.arange(captured, dtype=torch.float32)
        r = torch.sqrt(k) 
        theta = 2 * np.pi * self.phi_gold * k
        
        x = r * torch.cos(theta)
        y = r * torch.sin(theta)
        z = torch.sin(k * 0.1) # Атомные слои
        
        return x.numpy(), y.numpy(), z.numpy(), captured, sig["color"]

    def run(self, element="Gold"):
        x, y, z, count, color = self.separate(element)
        
        fig = plt.figure(figsize=(10, 8), facecolor='black')
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('black')
        
        # Отрисовка чистого элемента
        ax.scatter(x, y, z, c=color, s=20, alpha=1, edgecolors='white', linewidth=0.1)
        
        plt.title(f"PURIFIED {element.upper()} (99.9%)\nAtoms captured: {count}", color='white')
        ax.axis('off')
        plt.show()

# Запуск для Золота
Purifier = ElementPurifierPro()
Purifier.run("Gold")

