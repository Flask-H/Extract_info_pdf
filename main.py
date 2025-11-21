# Multi-file Python extractor project
# The document below contains multiple files in a single textdoc. Each file starts with a
# header line of the form: ### FILE: <path>
# You can copy each section to its own file in the same project structure.


### FILE: main.py
"""
main.py - flujo completo
Uso: python main.py ruta_al_pdf
"""
import os
import sys
import json
from pathlib import Path

from common.ocr import load_text_from_pdf
from classifier.contract_classifier import classify_contract
from export.csv_exporter import write_csv
from export.json_exporter import write_json

# Parsers registry
PARSERS = {
    'peugeot': 'parsers.parse_peugeot',
    'santander': 'parsers.parse_santander',
    'stellantis': 'parsers.parse_stellantis',
    'generic': 'parsers.parse_generic',
}

#Define una función que identifica el parser del archivo
def import_parser(module_path):
    module = __import__(module_path, fromlist=['*'])
    return module


#=================================================
# PRIMER PASO: Procesamiento del PDF
#=================================================
def main(path_pdf):
    
    #path_pdf coge el valor de sys.argv[1]
    #Valida si la ruta introducida es correcta
    path_pdf = Path(path_pdf)
    #Convierte la ruta en un objeto Path (usa pathlib).
    if not path_pdf.exists():
        #.exists: funcion de python
        print(f"Error: {path_pdf} no existe")
        return
    
    # 1) Extraer texto (OCR si es necesario)
    print("[1/4] Extrayendo texto del PDF...")
    #Funcion "load_text..."= Viene de common/ocr.py.
    text = load_text_from_pdf(str(path_pdf))
        
    # 2) Clasificar contrato
    print("[2/4] Clasificando tipo de contrato...")
    #Funcion "classify_contract"= viene de classifier/contract_classifier.py.
    contract_type = classify_contract(text)
    print(f"Tipo detectado: {contract_type}")

    # 3) Llamar al parser apropiado
    #Obtiene el parser adecuado
    
    parser_module = PARSERS.get(contract_type, PARSERS['generic'])
    #Función "import_parser"= creada en main.py
    parser = import_parser(parser_module)
    print(f"[3/4] Parseando con: {parser_module}")
    #funcion "parse"= introducida en cada documento de parsers, dependiendo del tipo de contrato previamente clasificado
    data = parser.parse(text)

    # 4) Normalizar y exportar
    out_dir = Path('output')
    out_dir.mkdir(exist_ok=True)
    csv_path = out_dir / (path_pdf.stem + '.csv')
    json_path = out_dir / (path_pdf.stem + '.json')

    print('[4/4] Exportando resultados...')
    write_csv([data], csv_path)
    write_json(data, json_path)

    print('\n✅ Extracción finalizada')
    print(f'CSV: {csv_path}')
    print(f'JSON: {json_path}')
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Uso: python main.py <ruta_pdf>')
        sys.exit(1)
    main(sys.argv[1])
