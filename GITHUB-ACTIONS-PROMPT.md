# 🚀 Готовый промт для запуска анализа данных

## Ситуация
- **Пользователь:** Вы (внешняя система)
- **Задача:** Запустить анализ Excel данных через GitHub Actions
- **Проблема:** Локально в Docker не работает (pandas не установлен)
- **Решение:** GitHub Actions автоматически установит все зависимости

---

## 📋 Что делать (по шагам):

### 1. Откройте GitHub Actions

Перейдите по адресу:
```
https://github.com/IlyaK86/workspace/actions
```

### 2. Выберите workflow

В списке workflows найдите и кликайте:
```
✅ Analyze Excel Report
```

### 3. Запустите workflow

- Нажмите кнопку **"Run workflow"**
- В поле "Branch" выберите: **main**
- (Опционально) В поле "Excel file" оставьте: **data/current_data.xlsx**
- Нажмите зеленую кнопку **"Run workflow"**

### 4. Подождите выполнения

- Запущенный workflow будет отображаться в списке
- Статус: **running** ⏳ (~2-3 минуты)
- Кликайте на него для просмотра логов

### 5. Проверьте логи выполнения

В разделе **"Steps"** вы увидите:
```
✅ Checkout code
✅ Set up Python
✅ Install dependencies (pandas, numpy, matplotlib, ...)
✅ Test libraries
✅ Create sample data if not exists
✅ Run analysis
✅ Upload artifacts
✅ Deploy to GitHub Pages
```

### 6. Скачайте результаты

После успешного выполнения:
- Вверху отчета нажмите **"Artifacts"**
- Скачайте ZIP-архив с файлами:
  - `reports/` - HTML дашборды
  - `output/` - Excel отчеты

---

## 🌐 Результаты будут доступны:

### 1. **GitHub Pages** (публикация)
```
https://ilyak86.github.io/workspace/
```

### 2. **Артефакты** (файлы для скачивания)
- Нажмите на успешный workflow run
- Внизу найдите **"Artifacts"**
- Скачайте архив

### 3. **Визуализация**
- HTML Dashboard с интерактивными графиками
- Excel отчет с KPI метриками
- JSON анализ

---

## 📊 Что произойдет автоматически:

1. **GitHub Actions** создаст виртуальное окружение с Python 3.11
2. **Установит все библиотеки:**
   - pandas, numpy, scipy
   - matplotlib, seaborn, plotly
   - scikit-learn, statsmodels
   - openpyxl
3. **Создаст тестовые данные** (если нет ваших)
4. **Запустит анализ:**
   - Проверка качества данных
   - Корреляции
   - Статистика
   - Визуализация
5. **Создаст отчеты:**
   - HTML Dashboard
   - Excel отчет
   - JSON анализ
6. **Деплоит на GitHub Pages**

---

## 🔧 Если что-то пойдет не так:

### Проблема: Ошибка при установке
**Решение:** Проверьте логи - обычно `pip install` работает автоматически

### Проблема: Нет тестовых данных
**Решение:** Workflow автоматически создаст пример данных

### Проблема: Ошибка в Python коде
**Решение:** 
1. Посмотрите логи ошибки
2. Проверьте код в workspace
3. Отправьте исправление через git push

---

## 🎯 Файлы в repo:

```
✅ src/excel_handler.py         - Загрузка данных из Excel
✅ src/excel_analytics.py       - Анализ и отчеты
✅ src/advanced_analytics.py    - Профессиональная аналитика
✅ src/advanced_visualize.py    - KPI дашборды
✅ .github/workflows/analyze-excel.yml - Workflow для запуска
✅ .github/workflows/install-deps.yml  - Установка зависимостей
✅ data/                        - Папка для данных
✅ output/                      - Результаты анализа
✅ reports/                     - HTML отчеты
```

---

## 📈 Ожидаемый результат:

После выполнения вы получите:

1. **HTML Dashboard** (`reports/dashboard_*.html`)
   - KPI карточки
   - Интерактивные Plotly графики
   - Корреляционные тепловые карты
   - Адаптивный дизайн

2. **Excel отчет** (`output/analysis_*.xlsx`)
   - Summary Statistics
   - Correlations
   - Data Quality
   - Original Data

3. **JSON анализ** (`output/analysis_*.json`)
   - Полная статистика
   - Метрики качества
   - Рекомендации

4. **GitHub Pages** (`https://ilyak86.github.io/workspace/`)
   - Веб-страница с отчетами
   - Доступна для всех

---

## 💡 Совет:

**Хотите анализировать СВОИ данные?**

1. Подготовьте Excel файл с вашими данными
2. Загрузите в репозиторий:
   ```bash
   # Создайте .env файл с вашим токеном
   # Или используйте GitHub web UI для upload файла
   ```
3. Запустите workflow с указанием вашего файла:
   - В `analyze-excel.yml` измените `excel_file` на ваш путь
4. Запустите workflow снова

---

## ✅ Итог:

**Все готово!** Просто:
1. ✅ Откройте GitHub Actions
2. ✅ Запустите workflow
3. ✅ Подождите 2-3 минуты
4. ✅ Скачайте или просмотрите результаты

**Система готова к работе!** 🚀

---

**Успешного запуска!** 🎯
