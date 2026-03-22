#!/usr/bin/env python3
"""
Тестовый скрипт - создает тестовые данные если нет Excel
"""
import pandas as pd
import numpy as np
from pathlib import Path
import os

# Создаем тестовые данные
def create_test_data():
    print("📊 Создаю тестовые данные...")
    
    # Данные о продажах
    dates = pd.date_range("2026-01-01", periods=30)
    categories = ["A", "B", "C", "D", "E"]
    regions = ["North", "South", "East", "West"]
    
    df = pd.DataFrame({
        'Date': dates,
        'Category': np.random.choice(categories, 30),
        'Region': np.random.choice(regions, 30),
        'Product': [f'Product {i+1}' for i in range(30)],
        'Quantity': np.random.randint(10, 100, 30),
        'Price': np.random.uniform(100, 500, 30),
        'Revenue': np.random.randint(1000, 50000, 30)
    })
    
    # Добавляем немного trend
    df['Revenue'] = df['Revenue'] + np.arange(30) * 100
    
    # Пакетно
    output_dir = Path("/home/openclaw/.openclaw/workspace/data")
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "test_data.xlsx"
    df.to_excel(output_file, index=False, engine='openpyxl')
    
    print(f"✅ Тестовый файл создан: {output_file}")
    print(f"📊 Строк: {len(df)}, Столбцов: {len(df.columns)}")
    
    return output_file

if __name__ == "__main__":
    try:
        print("=" * 60)
        print("🧪 ТЕСТ: Создание Excel файла")
        print("=" * 60)
        
        file_path = create_test_data()
        
        print("\n" + "=" * 60)
        print("🎉 ТЕСТ ЗАВЕРШЕН УСПЕШНО!")
        print("=" * 60)
        
    except ImportError as e:
        print(f"\n❌ ОШИБКА: pandas не установлен: {e}")
        print("Это ожидаемо в Docker-контейнере!")
        print("\nРешение: Запустить через GitHub Actions")
