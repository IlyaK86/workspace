#!/usr/bin/env python3
"""
Сбор данных из источника
Измени этот скрипт для твоего источника данных

Примеры:
- API (requests)
- Парсинг сайта (BeautifulSoup)
- База данных (SQLAlchemy)
- CSV/JSON файлы
"""

import requests
import pandas as pd
from datetime import datetime
import os

def fetch_data():
    print(f"[{datetime.now()}] Начало сбора данных...")
    
    # ЗАМЕНИ ЭТОТ КОД НА ТВОЙ ИСТОЧНИК ДАННЫХ!
    # Пример:
    # response = requests.get("https://api.example.com/data")
    # data = response.json()
    
    # Для теста - демо-данные:
    data = {
        "date": ["2026-03-20", "2026-03-21", "2026-03-22"],
        "value": [100, 150, 200],
        "category": ["A", "B", "C"]
    }
    
    df = pd.DataFrame(data)
    
    # Сохраняем в data/
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/current_data.csv", index=False)
    
    print(f"[{datetime.now()}] Данные сохранены в data/current_data.csv")
    print(f"Строк: {len(df)}, Столбцов: {len(df.columns)}")
    return df

if __name__ == "__main__":
    fetch_data()
