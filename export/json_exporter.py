### FILE: export/json_exporter.py
"""
Exportar un diccionario a JSON
"""
import json


def write_json(obj, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f'JSON escrito en {path}')
