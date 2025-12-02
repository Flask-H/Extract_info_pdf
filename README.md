### FILE: README.md
"""
Proyecto: Extract_info_pdf
Descripción: Sistema modular para extraer datos de contratos y otros documentos, generando archivos csv acumulables.
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
 - app/gui.py
 - app/worker.py
 - app/styles/dark_theme.py
 - run_gui.py
 - start_gui.bat
 - requirements.txt

Instrucciones para lanzar comando:
1. Crear un entorno virtual: python -m venv venv && source venv/bin/activate
2. Instalar dependencias: pip install -r requirements.txt
3. Ejecutar: python main.py <ruta_pdf>  # genera output/output.csv y output/output.json

Instrucciones para abrir interfaz usuario:
1. Colocar ruta de python local
2. Colocar ruta de carpeta de output local
3. Doble click sobre el archivo "start_gui.bat"
"""
