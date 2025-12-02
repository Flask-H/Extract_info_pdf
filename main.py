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
    'certificado_deuda': 'parsers.parse_cert_deuda',
}

#Define una función que identifica el parser del archivo
def import_parser(module_path):
    module = __import__(module_path, fromlist=['*'])
    return module


def procesar_carpeta(path_folder, gui_log_callback=None, gui_progress_callback=None):
    path_folder = Path(path_folder)

    # Helper interno para logs
    def log(msg):
        print(msg)
        if gui_log_callback:
            gui_log_callback(msg)

    # Helper interno para progreso
    def progress(value):
        if gui_progress_callback:
            gui_progress_callback(value)

    log(f" Procesando carpeta: {path_folder}")

    pdf_file = None
    docx_file = None

    # -------------------------
    # Identificar archivos
    # -------------------------
    files = list(path_folder.iterdir())
    total = len(files)
    current = 0

    for archivo in files:
        current += 1
        progress(int((current / total) * 30))  # primero 30% del progreso

        ext = archivo.suffix.lower()

        if ext == ".pdf":
            pdf_file = archivo

        elif ext == ".docx" and not archivo.name.startswith("~$") and "lock" not in archivo.name:
            docx_file = archivo

    if not pdf_file:
        log(" ❌ No hay PDF principal en la carpeta.")
        return

    # -------------------------
    # Procesar PDF (contrato)
    # -------------------------
    log(f"\n=== Procesando contrato PDF: {pdf_file.name} ===")
    from common.ocr import load_text_from_pdf
    text_pdf = load_text_from_pdf(str(pdf_file))

    from classifier.contract_classifier import classify_contract
    tipo = classify_contract(text_pdf)

    parser_module = PARSERS.get(tipo, PARSERS["generic"])
    parser = import_parser(parser_module)
    data = parser.parse(text_pdf)

    progress(60)

    # -------------------------
    # Procesar DOCX (certificado deuda)
    # -------------------------
    if docx_file:
        log(f"\n=== Procesando certificado deuda DOCX: {docx_file.name} ===")
        from common.docx_reader import extract_text_from_docx
        from parsers.parse_cert_deuda import parse as parse_cert

        text_docx = extract_text_from_docx(str(docx_file))
        deuda_data = parse_cert(text_docx)

        if deuda_data.get("cuantia"):
            data["cuantia"] = deuda_data["cuantia"]
            log(f" → Cuantía detectada: {data['cuantia']}")
        else:
            data["cuantia"] = None
            log(" → No se pudo extraer cuantía del DOCX")
    else:
        log("\n No se encontró archivo DOCX de certificado.")
        data["cuantia"] = None

    progress(85)

    # -------------------------
    # Exportar único archivo final
    # -------------------------
    out_dir = Path("C:/Users/Usuario/Documents/Proyecto_Output/")
    out_dir.mkdir(exist_ok=True)

    out_name = pdf_file.stem  # nombre del contrato
    csv_path = out_dir / (out_name + ".csv")
    json_path = out_dir / (out_name + ".json")

    write_csv([data], csv_path)
    write_json(data, json_path)

    log(f"\n Archivo combinado generado:")
    log(f"   CSV → {csv_path}")
    log(f"   JSON → {json_path}")

    progress(100)
    
def main(ruta):
    ruta = Path(ruta)

    if not ruta.exists():
        print(f" La ruta no existe: {ruta}")
        return

    if ruta.is_file():
        print(f" No está permitido procesar archivos unicos")
        return
    elif ruta.is_dir():
        procesar_carpeta(ruta)

    else:
        print(" La ruta no es ni archivo ni carpeta válida.")


# ==================================================
# EJECUCIÓN POR TERMINAL
# ==================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py <ruta_archivo_o_carpeta>")
        sys.exit(1)

    main(sys.argv[1])