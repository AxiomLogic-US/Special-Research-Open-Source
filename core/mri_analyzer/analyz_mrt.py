import numpy as np
import cv2
import matplotlib.pyplot as plt
import os

def analyze_universal_medical_v6(image_path, sensitivity=2.8):
    if not os.path.exists(image_path):
        print(f"❌ Файл {image_path} не найден!")
        return
    
    # 1. Загрузка
    img_array = np.fromfile(image_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)
    rows, cols = img.shape

    # 2. Подготовка (Улучшаем детализацию тканей)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(img)
    denoised = cv2.fastNlMeansDenoising(enhanced, None, h=10, templateWindowSize=7, searchWindowSize=21)

    # 3. Математика P=NP (Резонанс фазы)
    phi = (1 + 5**0.5) / 2
    x, y = np.meshgrid(np.arange(cols), np.arange(rows))
    harmonic_field = np.exp(1j * (x * phi + y) / phi)
    
    # Вычисляем отклонение (Im-часть)
    complex_map = denoised * harmonic_field
    anomaly_map = np.abs(np.imag(complex_map))
    
    # Возвращаем ту самую визуализацию через нормализацию
    # Мы не используем логарифм, чтобы картинка была контрастной, как раньше
    visual_map = cv2.normalize(anomaly_map, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # 4. Умная маска (Игнорируем белое и черное)
    tissue_mask = cv2.inRange(img, 25, 230)
    visual_map = cv2.bitwise_and(visual_map, visual_map, mask=tissue_mask)

    # 5. Детекция (Поиск разрывов)
    # Сглаживаем, чтобы объединить точки в очаги патологии
    blurred = cv2.GaussianBlur(visual_map, (13, 13), 0)
    mean_v, std_v = cv2.meanStdDev(blurred, mask=tissue_mask)
    
    # Порог: если хочешь больше контуров, уменьши sensitivity до 1.5
    _, mask = cv2.threshold(blurred, mean_v[0][0] + sensitivity * std_v[0][0], 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Рисуем результат
    result = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(result, contours, -1, (0, 0, 255), 2)

    # 6. Визуализация (Цветовая гамма "PLASMA" - она дает тот самый фиолетово-красный эффект)
    plt.figure(figsize=(18, 6))
    
    plt.subplot(1, 3, 1)
    plt.imshow(img, cmap='gray')
    plt.title("1. Оригинал")
    plt.axis('off')

    plt.subplot(1, 3, 2)
    # Используем 'plasma' или 'inferno' для того самого неонового вида
    plt.imshow(visual_map, cmap='plasma') 
    plt.title("2. Карта Дисгармонии (Im)")
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    plt.title("3. Локализация патологий")
    plt.axis('off')

    plt.tight_layout()
    plt.show()

    # Считаем индекс
    anomaly_area = (np.sum(mask > 0) / np.sum(tissue_mask > 0)) * 100
    print(f"✅ Анализ завершен.")
    print(f"📊 Индекс дисгармонии организма: {anomaly_area:.2f}%")

# Вызов
analyze_universal_medical_v6('mri.jpg', sensitivity=2.2)

