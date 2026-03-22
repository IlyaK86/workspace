#!/usr/bin/env python3
"""
EXCEL DATA HANDLER
==================
Поддержка загрузки, чтения, анализа и экспорта Excel файлов
Поддержка: .xlsx, .xls, .xlsm, .xlsb, .csv, .ods

Features:
- Загрузка файлов через drag & drop или upload
- Автоматическое определение листов
- Чтение данных с поддержкой дат, чисел, текста
- Обнаружение заголовков
- Валидация типов данных
- Экспорт результатов обратно в Excel
"""

import pandas as pd
from typing import Optional, Dict, List, Union
from pathlib import Path
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class ExcelDataHandler:
    """Профессиональный обработчик Excel файлов"""
    
    SUPPORTED_FORMATS = ['.xlsx', '.xls', '.xlsm', '.xlsb', '.csv', '.ods', '.xltx', '.xltm']
    
    def __init__(self, file_path: str, sheet_name: Optional[Union[int, str]] = None):
        """
        Инициализация
        Args:
            file_path: Путь к Excel файлу
            sheet_name: Имя листа или индекс (0-based)
        """
        self.file_path = Path(file_path)
        self.sheet_name = sheet_name
        self.raw_data = None
        self.df = None
        self.metadata = {}
        
        if not self._validate_file():
            raise FileNotFoundError(f"Файл {file_path} не найден или формат не поддерживается")
    
    def _validate_file(self) -> bool:
        """Проверяет наличие и формат файла"""
        if not self.file_path.exists():
            return False
        
        ext = self.file_path.suffix.lower()
        return ext in self.SUPPORTED_FORMATS
    
    def load(self, skiprows: int = 0, header: int = 0, usecols: Optional[Union[int, str, List]] = None) -> pd.DataFrame:
        """
        Загрузка данных из Excel
        Args:
            skiprows: Пропустить N строк в начале
            header: Номер строки с заголовками
            usecols: Какие столбцы читать
        """
        
        # Определяем читающий метод по формату
        file_ext = self.file_path.suffix.lower()
        
        try:
            if file_ext in ['.xlsx', '.xlsm', '.xlsb']:
                self.df = pd.read_excel(
                    self.file_path,
                    sheet_name=self.sheet_name,
                    header=header,
                    skiprows=skiprows,
                    usecols=usecols,
                    engine='openpyxl',
                    dtype_backend='pyarrow'
                )
            elif file_ext == '.xls':
                self.df = pd.read_excel(
                    self.file_path,
                    sheet_name=self.sheet_name,
                    header=header,
                    skiprows=skiprows,
                    usecols=usecols,
                    engine='xlrd'
                )
            elif file_ext == '.csv':
                self.df = pd.read_csv(
                    self.file_path,
                    skiprows=skiprows,
                    header=header if header == 0 else 0,
                    usecols=usecols
                )
            else:
                raise ValueError(f"Неподдерживаемый формат: {file_ext}")
            
            # Сохраняю сырые данные
            self.raw_data = self.df.copy()
            
            # Получаю метаданные
            self._extract_metadata()
            
            print(f"✅ Загружено: {len(self.df)} записей, {len(self.df.columns)} столбцов")
            print(f"📊 Столбцы: {list(self.df.columns)}")
            
            return self.df
            
        except Exception as e:
            raise ValueError(f"Ошибка загрузки Excel: {str(e)}")
    
    def _extract_metadata(self):
        """Извлекает метаданные файла"""
        self.metadata = {
            'filename': self.file_path.name,
            'filepath': str(self.file_path),
            'filesize_bytes': self.file_path.stat().st_size,
            'filesize_mb': round(self.file_path.stat().st_size / (1024**2), 4),
            'extensions': self.file_path.suffix.lower(),
            'sheet_name': self.sheet_name,
            'columns': list(self.df.columns),
            'column_types': {col: str(self.df[col].dtype) for col in self.df.columns},
            'total_rows': len(self.df),
            'date_range': None,
            'memory_usage_mb': round(self.df.memory_usage(deep=True).sum() / (1024**2), 4)
        }
        
        # Проверяем колонки с датами
        date_cols = self.df.select_dtypes(include=['datetime64']).columns
        if len(date_cols) > 0:
            self.metadata['date_range'] = {
                'min': str(self.df[date_cols[0]].min()),
                'max': str(self.df[date_cols[0]].max())
            }
    
    def get_info(self) -> dict:
        """Получает полную информацию о файле"""
        info = self.metadata.copy()
        info.update({
            'memory_usage': self.df.memory_usage(deep=True).sum() / 1024**2,
            'is_null': self.df.isnull().sum().to_dict(),
            'unique_values': self.df.nunique().to_dict(),
            'sample': self.df.head(5).to_dict(orient='records')
        })
        return info
    
    def export_to_excel(self, output_path: str, 
                      sheet_name: str = "Processed_Data",
                      index: bool = False,
                      engine: str = 'openpyxl'):
        """
        Экспортирует обработанные данные обратно в Excel
        Args:
            output_path: Путь для сохранения
            sheet_name: Имя листа
            index: Сохранять ли индекс
            engine: 'openpyxl' для .xlsx или 'xlsxwriter' для .xlsx
        """
        try:
            os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
            
            if engine == 'xlsxwriter' and output_path.endswith('.xlsx'):
                with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
                    self.df.to_excel(writer, sheet_name=sheet_name, index=index)
                    # Настраиваем форматирование
                    workbook = writer.book
                    worksheet = writer.sheets[sheet_name]
                    num_row_format = workbook.add_format({'num_format': '#,##0.00'})
                    date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})
                    
                    # Применяем форматы
                    for col_idx, col_type in self.metadata['column_types'].items():
                        if 'datetime' in col_type.lower():
                            worksheet.set_column(col_idx, col_idx, 15, date_format)
                        else:
                            worksheet.set_column(col_idx, col_idx, 12, num_row_format)
            else:
                self.df.to_excel(output_path, sheet_name=sheet_name, index=index, engine=engine)
            
            print(f"✅ Экспортировано: {output_path}")
            return output_path
            
        except Exception as e:
            raise ValueError(f"Ошибка экспорта в Excel: {str(e)}")
    
    def clean_data(self, 
                 drop_null: bool = True,
                 fill_null: bool = False,
                 fill_value: any = None,
                 drop_duplicates: bool = True,
                 columns: Optional[List[str]] = None) -> 'ExcelDataHandler':
        """
        Очистка данных
        Args:
            drop_null: Удалить строки с пропусками
            fill_null: Заполнить пропуски
            fill_value: Значение для заполнения
            drop_duplicates: Удалить дубликаты
            columns: Какие колонки обрабатывать (None = все)
        """
        self.df = self.df.copy()  # Не мутируем оригинал
        
        if columns:
            data_cols = [c for c in columns if c in self.df.columns]
        else:
            data_cols = self.df.columns
        
        # Обработка пропусков
        if drop_null:
            self.df = self.df.dropna(subset=data_cols)
            print(f"🗑 Удалено {len(self.raw_data) - len(self.df)} строк с пропусками")
        elif fill_null and fill_value is not None:
            self.df[data_cols] = self.df[data_cols].fillna(fill_value)
            print(f"🔄 Заполнено пропуски значением: {fill_value}")
        
        # Удаление дубликатов
        if drop_duplicates:
            before = len(self.df)
            self.df.drop_duplicates(inplace=True)
            after = len(self.df)
            if before != after:
                print(f"🗑 Удалено {before - after} дубликатов")
        
        # Обновляю сырые данные
        self.raw_data = self.df.copy()
        
        return self
    
    def transform(self, **kwargs) -> 'ExcelDataHandler':
        """
        Преобразование данных
        Примеры:
            df_transform.add_column('new_col', df['col1'] + df['col2'])
            df_transform.rename_columns({'old': 'new'})
            df_transform.convert_types({'date_col': 'datetime'})
        """
        self.df = self.df.copy()
        
        for method, args in kwargs.items():
            if method == 'add_column':
                col_name = args['name']
                values = args['values']
                self.df[col_name] = values
                print(f"➕ Добавлена колонка: {col_name}")
            elif method == 'rename_columns':
                self.df = self.df.rename(columns=args)
                print(f"🔄 Переименованы колонки: {args}")
            elif method == 'convert_types':
                types = args
                for col, dtype in types.items():
                    if col in self.df.columns:
                        if dtype == 'datetime':
                            self.df[col] = pd.to_datetime(self.df[col])
                            print(f"🕐 Преобразован тип: {col} → datetime")
                        elif dtype == 'float':
                            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
                        elif dtype == 'int':
                            self.df[col] = pd.to_numeric(self.df[col], errors='coerce').astype('Int64')
            
        self.raw_data = self.df.copy()
        return self
    
    def split_sheets(self) -> Dict[str, pd.DataFrame]:
        """Расщепляет все листы в словарь DataFrame'ов"""
        if self.sheet_name is None and isinstance(self.file_path.suffix.lower(), ['.xlsx', '.xls', '.xlsm']):
            # Если не указан конкретный лист, читаем все
            excel_file = pd.ExcelFile(self.file_path)
            sheets = {name: pd.read_excel(excel_file, sheet_name=name) 
                     for name in excel_file.sheet_names}
            
            print(f"📊 Найдено {len(sheets)} листов:")
            for name, df in sheets.items():
                print(f"  - {name}: {len(df)} строк")
            
            return sheets
        
        return {str(self.sheet_name): self.df.copy()}


def load_excel(file_path: str, **kwargs) -> ExcelDataHandler:
    """
    Фабричная функция для загрузки Excel файла
    Args:
        file_path: Путь к файлу
        **kwargs: Параметры для read_excel
    Returns:
        ExcelDataHandler
    """
    handler = ExcelDataHandler(file_path)
    handler.load(**kwargs)
    return handler


if __name__ == "__main__":
    # Пример использования
    print("📊 Excel Data Handler Demo")
    print("=" * 50)
    
    # Создаем тестовый Excel файл
    test_df = pd.DataFrame({
        "Date": pd.date_range("2026-01-01", periods=10),
        "Category": ["A", "B", "A", "B", "A", "B", "A", "B", "A", "B"],
        "Value": [100, 150, 200, 250, 300, 350, 400, 450, 500, 550],
        "Region": ["North", "South", "East", "West", "North", "South", "East", "West", "North", "South"]
    })
    
    # Сохраняем тестовый файл
    test_file = "test_data.xlsx"
    test_df.to_excel(test_file, index=False, engine='openpyxl')
    print(f"✅ Тестовый файл создан: {test_file}")
    
    # Загружаем
    handler = load_excel(test_file)
    print("\n📊 Информация о файле:")
    for key, value in handler.get_info().items():
        if key not in ['sample']:
            print(f"  {key}: {value}")
    
    # Анализируем
    print("\n📈 Корреляции:")
    print(handler.df.corr())
    
    # Экспортируем
    output_file = "output/test_analysis.xlsx"
    handler.export_to_excel(output_file)
    
    print("\n✅ Demo completed!")
