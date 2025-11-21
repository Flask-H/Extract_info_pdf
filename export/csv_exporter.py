### FILE: export/csv_exporter.py
"""
Exportar una lista de diccionarios a CSV (pandas por facilidad y robustez)
"""
import pandas as pd


def write_csv(rows, path):
    df = pd.DataFrame(rows)
    df.to_csv(path, index=False, encoding='utf-8')
    print(f'CSV escrito en {path}')

