# batch_processor.py

from pathlib import Path
from logger_config import get_logger
from processing import procesar_carpeta

logger = get_logger("BATCH")


def procesar_lote(
    carpeta_raiz,
    expediente_inicial,
    gui_log_callback=None,
    gui_progress_callback=None
):
    carpeta_raiz = Path(carpeta_raiz)

    logger.info("=== INICIANDO PROCESAMIENTO EN LOTE ===")

    contador = expediente_inicial

    #bucle procesamiento por carpetas
    for sub in carpeta_raiz.iterdir():
        if not sub.is_dir():
            continue

        logger.info(f"Procesando expediente {contador} → {sub.name}")

        procesar_carpeta(sub)
        contador += 1

    logger.info("=== Lote completado ===")
