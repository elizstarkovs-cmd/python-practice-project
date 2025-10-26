
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
news_analyzer.py

Консольный скрипт для анализа CSV-файла с новостями.
Использование:
    python news_analyzer.py path/to/news_data.csv

Выводит в консоль:
- Общее количество новостей
- Новость с максимальным количеством просмотров (заголовок и просмотры)
- Количество новостей в каждой категории (отсортировано по убыванию)
- Среднее количество просмотров на новость

Также формирует текстовый отчёт report.txt в той же папке, где находится CSV.
"""

import sys
import csv
import os
from collections import Counter

def read_csv(path):
    rows = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Проверка и приведение типов
            try:
                row['id'] = int(row['id'])
            except Exception:
                continue
            row['title'] = row.get('title', '').strip()
            row['category'] = row.get('category', '').strip()
            try:
                row['views'] = int(row.get('views', '0'))
            except Exception:
                row['views'] = 0
            row['publication_date'] = row.get('publication_date', '').strip()
            rows.append(row)
    return rows

def analyze(rows):
    total = len(rows)
    if total == 0:
        return {
            'total': 0,
            'top': None,
            'by_category': {},
            'avg_views': 0.0
        }
    top = max(rows, key=lambda r: r['views'])
    counts = Counter(r['category'] for r in rows)
    by_category = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    avg_views = sum(r['views'] for r in rows) / total
    return {
        'total': total,
        'top': top,
        'by_category': by_category,
        'avg_views': avg_views
    }

def format_report(analysis, csv_path):
    lines = []
    lines.append(f"Отчёт по файлу: {os.path.basename(csv_path)}")
    lines.append(f"Общее количество новостей: {analysis['total']}")
    if analysis['top']:
        lines.append(f"Новость с максимальным количеством просмотров: \"{analysis['top']['title']}\" — {analysis['top']['views']} просмотров")
    else:
        lines.append("Новость с максимальным количеством просмотров: отсутствует")
    lines.append("Количество новостей в каждой категории (по убыванию):")
    for cat, cnt in analysis['by_category']:
        lines.append(f"  {cat}: {cnt}")
    lines.append(f"Среднее количество просмотров на новость: {analysis['avg_views']:.2f}")
    return "\n".join(lines)

def main():
    if len(sys.argv) < 2:
        print("Ошибка: укажите путь к CSV-файлу как аргумент.")
        print("Пример: python news_analyzer.py news_data.csv")
        sys.exit(1)
    csv_path = sys.argv[1]
    if not os.path.exists(csv_path):
        print(f"Ошибка: файл не найден: {csv_path}")
        sys.exit(1)
    rows = read_csv(csv_path)
    analysis = analyze(rows)
    report_text = format_report(analysis, csv_path)
    print(report_text)
    # Сохранить отчёт рядом с CSV
    report_path = os.path.join(os.path.dirname(csv_path), "report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)
    # Выход с кодом 0
    return 0

if __name__ == "__main__":
    main()
