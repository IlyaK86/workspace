#!/usr/bin/env python3
"""
Обработка собранных данных
Агрегация, фильтрация, трансформация

Измени под свои задачи!
"""

import pandas as pd
from datetime import datetime
import os

def process_data():
    print(f"[{datetime.now()}] Начало обработки...")
    
    # Загружаем данные
    df = pd.read_csv("data/current_data.csv")
    
    # ТВОЯ ЛОГИКА обработки:
    # Пример - добавить колонку
    df["processed_date"] = datetime.now().strftime("%Y-%m-%d")
    
    # Пример - расчеты
    if "value" in df.columns:
        df["cumulative"] = df["value"].cumsum()
    
    # Пример - фильтрация/агрегация
    # df = df[df["value"] > 100]
    
    # Сохраняем обработанные данные
    os.makedirs("output", exist_ok=True)
    df.to_csv("output/processed_data.csv", index=False)
    
    print(f"[{datetime.now()}] Обработанные данные сохранены в output/processed_data.csv")
    return df

if __name__ == "__main__":
    process_data()
