# =============================================================================
# PRO ANALYTICS WORKFLOW - Consulting Level
# =============================================================================
## Используем профессиональные инструменты анализа данных

### 📦 1. Установи зависимости (GitHub Actions)
```bash
# GitHub Actions автоматически установит:
# - pandas, numpy, scipy (data processing)
# - matplotlib, seaborn, plotly (visualization)
# - scikit-learn, statsmodels (machine learning & stats)
# - jinja2, beautifulsoup4 (web reports)
```

### 🚀 2. Примеры использования

#### A. Профильный анализ с KPI Dashboard
```python
from src.advanced_visualize import generate_professional_report
import pandas as pd

# Загрузи свои данные
df = pd.read_csv("data/current_data.csv")

# Создай профессиональный отчет
report_file = generate_professional_report(df)
print(f"✅ Отчет: {report_file}")
```

**Результат:**
- Интерактивный HTML дашборд
- KPI карточки с метриками
- График трендов
- Круговая диаграмма категорий
- Тепловая карта корреляций
- Адаптивный дизайн

#### B. Продвинутая аналитика + инсайты
```python
from src.advanced_analytics import generate_consulting_report

# Комплексный анализ
insights = generate_consulting_report(df)

# Проверяем тренд
trend = insights['trend_analysis']
print(f"Тренд: {trend['trend_direction']} {trend['trend_strength']}")

# Генерируй текстовый отчет
report = df.apply(lambda x: generate_consulting_report).report_insights()
print(report)
```

**Включает:**
- Проверка качества данных
- Статистическое сведение
- Анализ распределения
- Корреляционный анализ
- Обнаружение аномалий
- Прогнозирование (ARIMA)

### 📊 3. Продвинутые функции

```python
# Статистические тесты
from scipy import stats
from statsmodels.tsa.arima.model import ARIMA
from sklearn.ensemble import RandomForestRegressor

# Аномалии (IQR метод)
def find_anomalies(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    return df[(df[column] < Q1 - 1.5*IQR) | (df[column] > Q3 + 1.5*IQR)]

# Корреляции
corr_matrix = df.corr()
strong_corr = corr_matrix[abs(corr_matrix) > 0.7]

# Прогнозирование
model = ARIMA(df['value'], order=(1,1,1))
forecast = model.forecast(steps=10)
```

### 🎯 4. Визуализация уровня Big4

```python
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Интерактивные диаграммы
fig = px.scatter(df, x='date', y='value', trendline='lowess')
fig.show()

# Heatmap корреляций
fig = px.imshow(corr_matrix, labels={'x': 'Column', 'y': 'Column', 'color': 'Correlation'})

# 3D поверхности
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X, Y, Z)
```

### 📁 Файловая структура

```
workspace/
├── src/
│   ├── fetch_data.py       # Сбор данных
│   ├── process_data.py     # Обработка
│   ├── visualize.py        # Базовая визуализация
│   ├── advanced_visualize.py  # PRO отчеты (KPI, интерактив)
│   └── advanced_analytics.py    # PRO аналитика (стат, ML, прогноз)
├── data/                   # Исходные данные
├── reports/                # Сгенерированные отчеты
├── output/                 # Обработанные данные
└── requirements.txt        # Библиотеки для установки
```

### 🌐 Публикация в GitHub Pages

После запуска:
```bash
python src/advanced_visualize.py
python src/advanced_analytics.py
```

GitHub Actions автоматически деплоит `reports/` на:
**https://ilyak86.github.io/workspace/reports/**

### 📈 Кнопки быстрого запуска

#### Ручной запуск:
```bash
python3 src/advanced_visualize.py
python3 src/advanced_analytics.py
```

#### Автоматически (каждый день в 12:00 UTC):
GitHub Actions запускает: `.github/workflows/auto-report.yml`

---

### 💡 Рекомендации

1. **Всегда проверяй качество данных** перед анализом
2. **Используй интерактивные графики** для презентаций
3. **Документируй инсайты** в текстовые отчёты
4. **Визуализируй аномалии** для проверки данных
5. **Прогнозируй тренды** для стратегического планирования

---

**Генерируй отчеты уровня консалтинговых компаний с помощью OpenClaw!** 🏆
