### FILE: README.md
"""
Proyecto: extractor_pipeline_python
Descripción: Sistema modular para detectar el tipo de contrato, extraer campos (nombre, dirección, CP, provincia, población, NIF, email, teléfono...) y exportar a CSV/JSON/TXT.
Estructura propuesta (cada archivo incluido en este textdoc):
 - main.py
 - common/ocr.py
 - common/cleaner.py
 - classifier/contract_classifier.py
 - parsers/parse_peugeot.py   (usa como base extractor_manteniment.py que subiste)
 - parsers/parse_santander.py
 - parsers/parse_stellantis.py
 - parsers/parse_generic.py
 - export/csv_exporter.py
 - export/json_exporter.py
 - requirements.txt

Instrucciones rápidas:
1. Crear un entorno virtual: python -m venv venv && source venv/bin/activate
2. Instalar dependencias: pip install -r requirements.txt
3. Ejecutar: python main.py <ruta_pdf>  # genera output/output.csv y output/output.json

"""
