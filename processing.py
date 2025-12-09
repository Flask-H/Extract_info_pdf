# processing.py

from pathlib import Path
from logger_config import get_logger

from common.ocr import load_text_from_pdf
from common.docx_reader import extract_text_from_docx

from classifier.contract_classifier import classify_contract
from export.csv_exporter import write_csv
from export.json_exporter import write_json

# importar parsers directamente (sin riesgo de ciclos)
import parsers.parse_peugeot as parse_peugeot
import parsers.parse_santander as parse_santander
import parsers.parse_stellantis as parse_stellantis
import parsers.parse_generic as parse_generic
import parsers.parse_cert_deuda as parse_cert_deuda

logger = get_logger("PROCESSING")

PARSERS = {
    "peugeot": parse_peugeot,
    "santander": parse_santander,
    "stellantis": parse_stellantis,
    "generic": parse_generic,
}


def procesar_carpeta(path_folder, gui_log_callback=None, gui_progress_callback=None):

    path_folder = Path(path_folder)

    # ----------------------------
    # Helper de logs
    # ----------------------------
    def log(msg):
        logger.info(msg)
        if gui_log_callback:
            gui_log_callback(msg)

    def progress(val):
        if gui_progress_callback:
            gui_progress_callback(val)

    log(f"Procesando carpeta: {path_folder}")

    pdf_file = None
    docx = None
    # ----------------------------
    # Detectar PDF y DOCX
    # ----------------------------
    pdf = next((f for f in path_folder.iterdir() if f.suffix.lower() == ".pdf"), None)
    docx = next((f for f in path_folder.iterdir() if f.suffix.lower() == ".docx"
                 and not f.name.startswith("~$")
                 and "lock" not in f.name), None)

    if not pdf:
        log(" No se encontró PDF principal")
        return None

    # ----------------------------
    # Proceso del contrato PDF
    # ----------------------------
    log(f"=== Leyendo PDF {pdf.name} ===")
    text_pdf = load_text_from_pdf(str(pdf))

    tipo = classify_contract(text_pdf)
    parser = PARSERS.get(tipo, parse_generic)

    log(f"→ Tipo detectado: {tipo}")
    data = parser.parse(text_pdf)

    progress(50)

    # ----------------------------
    # Proceso del certificado DOCX
    # ----------------------------
    if docx:
        log(f"=== Leyendo DOCX {docx.name} ===")
        text_docx = extract_text_from_docx(str(docx))
        deuda = parse_cert_deuda.parse(text_docx)

        data["cuantia"] = deuda.get("cuantia")
        log(f"→ Cuantía encontrada: {data['cuantia']}")
    else:
        log("No se encontró DOCX de certificado.")
        data["cuantia"] = None

    progress(80)

    # ----------------------------
    # Exportar salida
    # ----------------------------
    out_dir = Path("C:/Users/Usuario/Documents/Proyecto_Output/")
    out_dir.mkdir(exist_ok=True)

    out_name = pdf.stem  # nombre del contrato
    csv_path = out_dir / (out_name + ".csv")
    json_path = out_dir / (out_name + ".json")

    write_csv([data], csv_path)
    write_json(data, json_path)

    log(f"\n Archivo combinado generado:")
    log(f"   CSV → {csv_path}")
    log(f"   JSON → {json_path}")


    progress(100)

    return data
