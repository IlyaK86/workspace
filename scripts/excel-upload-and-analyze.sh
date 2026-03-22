#!/bin/bash
# =============================================================================
# EXCEL FILE UPLOAD & ANALYSIS
# =============================================================================
# Загрузка Excel файлов и их анализ
# =============================================================================

DATE=$(date +%Y%m%d_%H%M%S)
UPLOAD_DIR="/home/openclaw/.openclaw/workspace/data/uploads"
ANALYSIS_DIR="/home/openclaw/.openclaw/workspace/output/excel"

mkdir -p "$UPLOAD_DIR"
mkdir -p "$ANALYSIS_DIR"

echo "📁 Upload Directory: $UPLOAD_DIR"
echo "📊 Analysis Directory: $ANALYSIS_DIR"
echo ""

echo "📥 Drag & Drop Excel files to: $UPLOAD_DIR"
echo "Press Ctrl+C when done, then I'll analyze them..."
echo ""

# Ждем ввода пользователя
read -p "Press Enter when files are uploaded..."

# Находим все Excel файлы
echo ""
echo "🔍 Scanning for Excel files..."

EXCEL_FILES=$(find "$UPLOAD_DIR" -name "*.xlsx" -o -name "*.xls" -o -name "*.csv" 2>/dev/null)

if [ -z "$EXCEL_FILES" ]; then
    echo "❌ No Excel files found!"
    exit 1
fi

echo "✅ Found Excel files:"
echo "$EXCEL_FILES" | while read file; do
    echo "  - $(basename $file)"
done

echo ""
echo "🚀 Starting Analysis..."
echo ""

# Анализируем каждый файл
echo "$EXCEL_FILES" | while read excel_file; do
    if [ -f "$excel_file" ]; then
        filename=$(basename "$excel_file")
        echo "📊 Analyzing: $filename"
        
        # Запускаем Python скрипт анализа
        python3 << EOF
from src.excel_analytics import ExcelAnalyticsEngine

import sys
sys.path.insert(0, '/home/openclaw/.openclaw/workspace')

try:
    analyzer = ExcelAnalyticsEngine("$excel_file")
    analysis = analyzer.comprehensive_analysis()
    
    # Генерируем отчеты
    excel_report = analyzer.generate_excel_report(analysis)
    html_report = analyzer.generate_interactive_html_report(analysis)
    json_report = analyzer.save_analysis()
    
    print(f"\n✅ Analysis complete for: {filename}")
    print(f"  Rows: {analysis['loading']['rows']}")
    print(f"  Columns: {analysis['loading']['columns']}")
    print(f"  Quality: {analysis['data_quality']['data_quality_score']}")
    print(f"  Reports: {excel_report}, {html_report}")
    
except Exception as e:
    print(f"❌ Error analyzing {filename}: {str(e)}")
    sys.exit(1)
EOF
        
        echo ""
    fi
done

echo "✅ All Excel files analyzed!"
