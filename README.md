# 📊 OpenClaw Data Analysis Workspace

## Структура проекта

```
workspace/
├── src/                  # Python-скрипты для сбора и обработки данных
├── data/                 # Исходные данные (CSV, JSON, базы)
├── output/               # Промежуточные и финальные результаты
├── reports/              # GHP-страницы с отчетами
├── scripts/              # Shell-скрипты для автоматизации
├── notebooks/            # Jupyter notebooks для анализа
└── .github/workflows/    # Автоматический деплой на GitHub Pages
```

## 🚀 Быстрый старт

1. **Получить данные:** Создать скрипт в `src/fetch_data.py`
2. **Обработать:** В `src/process_data.py`
3. **Визуализировать:** В `src/visualize.py` или `notebooks/`
4. **Опубликовать:** GitHub Actions автоматически деплоит `reports/`

## 🔧 Настройка

- GitHub: https://github.com/IlyaK86/workspace
- Pages: https://ilyak86.github.io/workspace (после настройки в Settings)

## 📝 Добавить новые задачи

Создай файл в `scripts/new-automation.sh` для нового источника данных
