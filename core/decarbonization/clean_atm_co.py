import torch
import numpy as np
import matplotlib.pyplot as plt

class AtmosphericLaser:
    def __init__(self, air_density=200000):
        self.n = air_density
        self.phi_gold = (1 + 5**0.5) / 2
        
    def clean_air(self, target_omega_co2=4.3):
        # 1. Генерируем хаос молекул атмосферы (N2, O2, CO2)
        indices = torch.arange(self.n, dtype=torch.float32)
        # У каждой молекулы своя "фаза" (подпись)
        air_phases = (indices * self.phi_gold) % (2 * np.pi)
        
        # 2. Настройка лазера на Резонанс CO2
        # Ищем только те молекулы, которые "откликаются" на 4.3 мкм
        resonance = torch.cos(air_phases - (target_omega_co2 % (2 * np.pi)))
        
        # 3. Фильтр захвата (уничтожение/сборка CO2)
        # 0.9995 - экстремальная точность, чтобы не задеть кислород (O2)
        co2_mask = resonance > 0.9995
        captured_co2 = torch.sum(co2_mask).item()
        
        # Координаты "очищенного" углерода (собираем в структуру)
        k = torch.arange(captured_co2)
        z = torch.linspace(0, 5, captured_co2) # Столб лазерного луча
        r = 0.2 * torch.rand(captured_co2)
        theta = k * self.phi_gold
        
        x = r * torch.cos(theta)
        y = r * torch.sin(theta)
        
        return x.numpy(), y.numpy(), z.numpy(), captured_co2

    def show_cleaning(self):
        x, y, z, count = self.clean_air()
        
        fig = plt.figure(figsize=(10, 10), facecolor='black')
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('black')
        
        # Рисуем "Луч Лазера", который вытягивает углерод из неба
        ax.scatter(x, y, z, c=z, cmap='copper', s=5, alpha=0.6)
        
        plt.title(f"ATMOSPHERIC LASER CLEANER\nCO2 molecules neutralized: {count}", color='white')
        ax.axis('off')
        print(f"✅ Лазерный луч деактивировал {count} молекул CO2.")
        plt.show()

# Запуск системы очистки
cleaner = AtmosphericLaser()
cleaner.show_cleaning()

