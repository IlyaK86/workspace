#!/usr/bin/env python3
"""
EXCEL ANALYTICS REPORT ENGINE
==============================
Анализ Excel данных с профессиональными отчетами
Использует ExcelDataHandler для загрузки + ProfessionalReporter для визуализации
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import style
import seaborn as sns
from datetime import datetime
from pathlib import Path
import os
from typing import Dict, List, Optional, Any, Union

from src.excel_handler import ExcelDataHandler, load_excel
from src.advanced_analytics import ConsultingAnalytics
from src.advanced_visualize import ProfessionalReporter

class ExcelAnalyticsEngine:
    """Полный анализ Excel данных"""
    
    def __init__(self, excel_file: str, 
                sheet_name: Optional[Union[int, str]] = None,
                cleanup_kwargs: Dict = None):
        """
        Args:
            excel_file: Путь к Excel файлу
            sheet_name: Имя листа или индекс
            cleanup_kwargs: Параметры для очистки данных
        """
        self.excel_file = excel_file
        self.sheet_name = sheet_name
        self.cleanup_kwargs = cleanup_kwargs or {
            'drop_null': True,
            'fill_null': False,
            'drop_duplicates': True
        }
        
        # Загрузка
        self.handler = load_excel(excel_file, sheet_name=sheet_name)
        
        # Очистка
        self.handler.clean_data(**self.cleanup_kwargs)
        
        self.df = self.handler.df
        self.metadata = self.handler.metadata
        
        self.reports_dir = "reports/excel"
        self.output_dir = "output/excel"
        
        os.makedirs(self.reports_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        
    def comprehensive_analysis(self) -> Dict[str, Any]:
        """Комплексный анализ Excel данных"""
        
        analysis = {
            'loading': {
                'file': self.metadata['filename'],
                'sheets': self.metadata['sheet_name'],
                'rows': len(self.df),
                'columns': len(self.df.columns),
                'memory_mb': self.metadata['memory_usage_mb']
            },
            'data_quality': self._data_quality_check(),
            'summary_statistics': self._summary_statistics(),
            'correlations': self._correlation_analysis(),
            'categorical_analysis': self._categorical_analysis(),
            'missing_values': self._missing_values_check()
        }
        
        return analysis
    
    def _data_quality_check(self) -> Dict:
        """Проверка качества данных"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        object_cols = self.df.select_dtypes(include=['object']).columns
        
        return {
            'total_nulls': int(self.df.isnull().sum().sum()),
            'null_percentage': round(self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns)) * 100, 2),
            'duplicate_rows': int(self.df.duplicated().sum()),
            'numeric_columns': len(numeric_cols),
            'object_columns': len(object_cols),
            'datetime_columns': len(self.df.select_dtypes(include=['datetime']).columns),
            'data_quality_score': 'High' if self.df.isnull().sum().sum() == 0 else 'Medium' if self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns)) < 0.05 else 'Low'
        }
    
    def _summary_statistics(self) -> Dict:
        """Статистическое сведение числовых колонок"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            return {}
        
        stats = {}
        for col in numeric_cols:
            stats[col] = {
                'mean': float(self.df[col].mean()),
                'std': float(self.df[col].std()),
                'min': float(self.df[col].min()),
                'max': float(self.df[col].max()),
                'median': float(self.df[col].median()),
                'skewness': float(self.df[col].skew()),
                'kurtosis': float(self.df[col].kurtosis())
            }
        
        return stats
    
    def _correlation_analysis(self) -> Dict:
        """Корреляционный анализ"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) < 2:
            return {}
        
        corr_matrix = self.df[numeric_cols].corr()
        
        # Находим сильные корреляции
        strong_corr = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                if abs(corr_val) > 0.7:
                    strong_corr.append({
                        'column1': corr_matrix.columns[i],
                        'column2': corr_matrix.columns[j],
                        'correlation': float(corr_val)
                    })
        
        return {
            'correlation_matrix': corr_matrix,
            'strong_correlations': strong_corr[:10],
            'average_correlation': float(corr_matrix.values[~np.eye(len(corr_matrix),dtype=bool)].mean())
        }
    
    def _categorical_analysis(self) -> Dict:
        """Анализ категориальных переменных"""
        cat_cols = self.df.select_dtypes(include=['object']).columns
        
        if len(cat_cols) == 0:
            return {}
        
        categories = {}
        for col in cat_cols[:5]:  # Top 5 categorical columns
            value_counts = self.df[col].value_counts()
            categories[col] = {
                'unique_values': int(value_counts.nunique()),
                'most_common': value_counts.index[0] if len(value_counts) > 0 else None,
                'most_common_count': int(value_counts.iloc[0]) if len(value_counts) > 0 else 0,
                'distribution': value_counts.to_dict()
            }
        
        return categories
    
    def _missing_values_check(self) -> Dict:
        """Проверка пропущенных значений"""
        missing = self.df.isnull().sum()
        
        return {
            'total_missing': int(missing.sum()),
            'columns_with_missing': {col: int(missing[col]) for col in missing.index if missing[col] > 0},
            'missing_percentage': {col: float(missing[col] / len(self.df) * 100) for col in missing.index if missing[col] > 0}
        }
    
    def generate_excel_report(self, analysis: Dict = None) -> str:
        """Генерирует профессиональный Excel отчет с аналитикой"""
        
        if analysis is None:
            analysis = self.comprehensive_analysis()
        
        # Создаем сводный Excel отчет
        output_path = f"{self.output_dir}/analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        try:
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                # Страница 1: Summary Statistics
                summary_df = pd.DataFrame({
                    'Metric': ['Total Records', 'Total Columns', 'Memory Usage (MB)', 'Data Quality Score', 
                              'Total Nulls', 'Null %', 'Duplicate Rows', 'Date Range'],
                    'Value': [
                        analysis['loading']['rows'],
                        analysis['loading']['columns'],
                        analysis['loading']['memory_mb'],
                        analysis['data_quality']['data_quality_score'],
                        analysis['data_quality']['total_nulls'],
                        f"{analysis['data_quality']['null_percentage']}%",
                        analysis['data_quality']['duplicate_rows'],
                        'N/A'  # Упрощенно
                    ]
                })
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                # Страница 2: Correlations
                if len(analysis['correlations']) > 0 and 'correlation_matrix' in analysis['correlations']:
                    corr_df = pd.DataFrame(analysis['correlations']['correlation_matrix'])
                    corr_df.to_excel(writer, sheet_name='Correlations')
                
                # Страница 3: Data Quality
                quality_df = pd.DataFrame([
                    {
                        'Metric': 'Quality Score',
                        'Score': analysis['data_quality']['data_quality_score'],
                        'Total Nulls': analysis['data_quality']['total_nulls'],
                        'Null %': f"{analysis['data_quality']['null_percentage']}%"
                    }
                ])
                quality_df.to_excel(writer, sheet_name='Quality', index=False)
                
                # Страница 4: Statistics
                if len(analysis['summary_statistics']) > 0:
                    stats_list = []
                    for col, stats in analysis['summary_statistics'].items():
                        stats_list.append({
                            'Column': col,
                            'Mean': stats.get('mean', 'N/A'),
                            'Std': stats.get('std', 'N/A'),
                            'Min': stats.get('min', 'N/A'),
                            'Max': stats.get('max', 'N/A'),
                            'Median': stats.get('median', 'N/A')
                        })
                    
                    stats_df = pd.DataFrame(stats_list)
                    stats_df.to_excel(writer, sheet_name='Statistics', index=False)
                
                # Страница 5: Original Data
                self.df.to_excel(writer, sheet_name='Original_Data', index=False)
            
            print(f"✅ Excel отчет создан: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Ошибка создания Excel отчета: {str(e)}")
            raise
    
    def generate_interactive_html_report(self, analysis: Dict = None) -> str:
        """Генерирует интерактивный HTML дашборд"""
        
        if analysis is None:
            analysis = self.comprehensive_analysis()
        
        # Создаем профессиональный дашборд
        reporter = ProfessionalReporter(self.df)
        html_file = reporter.create_kpi_dashboard()
        
        print(f"✅ HTML отчет создан: {html_file}")
        return html_file
    
    def save_analysis(self) -> str:
        """Сохраняет результаты анализа в JSON"""
        output_path = f"{self.output_dir}/analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Конвертируем в JSON
        analysis_dict = {}
        for key, value in self.comprehensive_analysis().items():
            if isinstance(value, dict):
                analysis_dict[key] = {k: (v.tolist() if hasattr(v, 'tolist') else v) for k, v in value.items()}
            else:
                analysis_dict[key] = value
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_dict, f, indent=4, ensure_ascii=False)
        
        print(f"✅ JSON анализ сохранен: {output_path}")
        return output_path


def analyze_excel(file_path: str, **kwargs) -> Dict:
    """Фабричная функция для анализа Excel"""
    analyzer = ExcelAnalyticsEngine(file_path, **kwargs)
    return analyzer.comprehensive_analysis()


if __name__ == "__main__":
    # Тест
    print("📊 Excel Analytics Demo")
    print("=" * 50)
    
    # Создаем тестовый файл
    test_df = pd.DataFrame({
        "Date": pd.date_range("2026-01-01", periods=50),
        "Category": np.random.choice(["A", "B", "C"], 50),
        "Region": np.random.choice(["North", "South", "East"], 50),
        "Value": np.random.randn(50).cumsum() + 100,
        "Quantity": np.random.randint(10, 100, 50)
    })
    
    test_file = "test_excel.xlsx"
    test_df.to_excel(test_file, index=False, engine='openpyxl')
    print(f"✅ Тестовый файл: {test_file}")
    
    # Анализируем
    analyzer = ExcelAnalyticsEngine(test_file)
    analysis = analyzer.comprehensive_analysis()
    
    print("\n📊 Data Quality:")
    print(f"  Quality Score: {analysis['data_quality']['data_quality_score']}")
    print(f"  Total Nulls: {analysis['data_quality']['total_nulls']}")
    
    print("\n📈 Summary Statistics:")
    for col, stats in analysis['summary_statistics'].items():
        print(f"  {col}: Mean={stats['mean']:.2f}, Std={stats['std']:.2f}")
    
    # Генерируем отчеты
    print("\n📝 Создаем отчеты...")
    excel_report = analyzer.generate_excel_report(analysis)
    html_report = analyzer.generate_interactive_html_report(analysis)
    
    print(f"\n✅ Все отчеты готовы!")
    print(f"  Excel: {excel_report}")
    print(f"  HTML: {html_report}")
