# 📊 Excel Support - Полная поддержка Excel файлов

## 🎯 Что умеет система

- ✅ **Загрузка** Excel файлов (.xlsx, .xls, .xlsm, .csv)
- ✅ **Анализ** данных с профессиональными метриками
- ✅ **Очистка** данных (nulls, duplicates)
- ✅ **Визуализация** KPI дашбордов
- ✅ **Экспорт** результатов в Excel
- ✅ **HTML отчеты** с интерактивными графиками

## 🚀 Быстрый старт

### 1. Загрузи Excel файл

```bash
# Создание папки для загрузки
mkdir -p /home/openclaw/.openclaw/workspace/data/uploads

# Помести свои Excel файлы в эту папку
# Или используй drag & drop через файловый менеджер
```

### 2. Запусти анализ

```bash
cd /home/openclaw/.openclaw/workspace
bash scripts/excel-upload-and-analyze.sh
```

**Нажми Enter** когда файлы загружены, и начинается анализ!

## 📋 Python API

### Загрузка файла:

```python
from src.excel_handler import load_excel

# Базовая загрузка
handler = load_excel("data/my_file.xlsx")
print(handler.df)

# Загрузка конкретного листа
handler = load_excel("data/my_file.xlsx", sheet_name="Sheet1")
print(handler.df)

# Пропуск строк
handler.load(skiprows=2, header=0)
```

### Очистка данных:

```python
# Удалить nulls
handler.clean_data(drop_null=True)

# Заполнить nulls
handler.clean_data(fill_null=True, fill_value=0)

# Удалить дубликаты
handler.clean_data(drop_duplicates=True)
```

### Превращение данных:

```python
# Добавить колонку
handler.transform(
    add_column={
        'name': 'Total',
        'values': handler.df['Col1'] + handler.df['Col2']
    }
)

# Переименовать колонки
handler.transform(
    rename_columns={'OldName': 'NewName'}
)

# Преобразовать типы
handler.transform(
    convert_types={
        'DateCol': 'datetime',
        'ValueCol': 'float'
    }
)
```

### Экспорт:

```python
# Экспортировать в Excel
handler.export_to_excel(
    output_path="output/processed.xlsx",
    sheet_name="Processed",
    engine='openpyxl'
)
```

## 📊 Анализ с отчетами

```python
from src.excel_analytics import ExcelAnalyticsEngine

# Создай аналитик
analyzer = ExcelAnalyticsEngine(
    excel_file="data/my_file.xlsx",
    cleanup_kwargs={
        'drop_null': True,
        'fill_null': False,
        'drop_duplicates': True
    }
)

# Получи комплексный анализ
analysis = analyzer.comprehensive_analysis()

# Генерируй отчеты
excel_report = analyzer.generate_excel_report(analysis)  # Excel
html_report = analyzer.generate_interactive_html_report(analysis)  # HTML
json_report = analyzer.save_analysis()  # JSON
```

## 📊 Что включено в анализ

### 1. **Data Quality Score**
- Проверка nulls
- Обнаружение дубликатов
- Оценка качества данных

### 2. **Статистика**
- Mean, Std, Min, Max, Median
- Skewness, Kurtosis
- Корреляции между колонками

### 3. **Категориальный анализ**
- Count уникальных значений
- Распределение категорий
- Most common values

### 4. **Пропущенные значения**
- Перечень колонок с пропусками
- Процент пропусков
- Рекомендации по заполнению

## 🔧 Форматы файлов

Поддерживаются форматы:
- `.xlsx` (Office Excel 2007+)
- `.xls` (Old Excel)
- `.xlsm` (Макросы)
- `.xlsb` (Бинарный)
- `.csv` (Comma Separated Values)
- `.ods` (OpenDocument)

## 🌐 Публикация в GitHub Pages

После анализа отчеты автоматически публикуются на:
**https://ilyak86.github.io/workspace/reports/excel/**

## 💡 Примеры использования

### Пример 1: Анализ продаж

```python
from src.excel_analytics import ExcelAnalyticsEngine

analyzer = ExcelAnalyticsEngine(
    excel_file="data/sales.xlsx",
    cleanup_kwargs={
        'drop_null': True,
        'fill_null': False
    }
)

analysis = analyzer.comprehensive_analysis()

# Проверяем корреляцию между ценой и количеством
if 'correlations' in analysis:
    print(analysis['correlations']['correlation_matrix'])
```

### Пример 2: Очистка и экспорт

```python
from src.excel_handler import load_excel

handler = load_excel("data/raw_data.xlsx")

# Очистка
handler.clean_data(
    drop_null=True,
    fill_null=False,
    drop_duplicates=True
)

# Экспорт
handler.export_to_excel("output/clean_data.xlsx")
```

## 📁 Файловая структура

```
workspace/
├── data/
│   └── uploads/              # Загрузка Excel файлов
├── output/
│   └── excel/                # Результаты анализа
├── reports/
│   └── excel/                # HTML отчеты
├── src/
│   ├── excel_handler.py      # Основная логика
│   └── excel_analytics.py    # Анализа и отчеты
└── scripts/
    └── excel-upload-and-analyze.sh  # CLI утилита
```

## 🎯 Рекомендации

1. **Всегда проверяй качество данных** перед анализом
2. **Используй интерактивные отчеты** для презентаций
3. **Документируй инсайты** в текстовые отчеты
4. **Экспортируй результаты** в Excel для командной работы
5. **Используй GitHub Actions** для автоматизации

---

**Система анализа Excel уровня Big4 готова к работе!** 🏆
