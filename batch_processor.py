# batch_processor.py

from pathlib import Path
from logger_config import get_logger
from processing import procesar_carpeta
from export.csv_exporter import write_csv
from export.json_exporter import write_json

logger = get_logger("BATCH")


def procesar_lote(
    carpeta_raiz,
    expediente_inicial,
    gui_log_callback=None,
    gui_progress_callback=None
):

    carpeta_raiz = Path(carpeta_raiz)
    logger.info("=== INICIANDO PROCESAMIENTO EN LOTE ===")

    if gui_log_callback:
        gui_log_callback("=== INICIANDO PROCESAMIENTO EN LOTE ===")

    contador = expediente_inicial
    filas = []   # <-- AQUI SE ACUMULAN LAS FILAS DEL CSV COMBINADO

    subcarpetas = [d for d in carpeta_raiz.iterdir() if d.is_dir()]
    total = len(subcarpetas)
    actual = 0

    for sub in subcarpetas:
        actual += 1

        # progreso (20% al 90%)
        if gui_progress_callback:
            gui_progress_callback(int(20 + (actual / total) * 70))

        logger.info(f"Procesando expediente {contador} → {sub.name}")
        if gui_log_callback:
            gui_log_callback(f"Procesando expediente {contador} → {sub.name}")

        datos = procesar_carpeta(
            sub,
            gui_log_callback=gui_log_callback,
            gui_progress_callback=gui_progress_callback
        )

        if datos:
            datos["expediente"] = contador
            filas.append(datos)

        contador += 1

    # ================================
    #  EXPORTAR ARCHIVO COMBINADO
    # ================================
    out_dir = Path("C:/Users/Usuario/Documents/Proyecto_Output/")
    out_dir.mkdir(exist_ok=True)

    path_csv = out_dir / "resultado_combinado.csv"
    path_json = out_dir / "resultado_combinado.json"

    write_csv(filas, path_csv)
    write_json(filas, path_json)

    msg = f"✔ Archivo combinado generado:\n CSV → {path_csv}\n JSON → {path_json}"
    logger.info(msg)
    if gui_log_callback:
        gui_log_callback(msg)

    if gui_progress_callback:
        gui_progress_callback(100)

    return filas
