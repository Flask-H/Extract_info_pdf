##FILE: app/worker.py
from PySide6.QtCore import QObject, Signal
from processing import procesar_carpeta
from batch_processor import procesar_lote
from logger_config import get_logger

logger = get_logger("WORKER")

class Worker(QObject):
    progress = Signal(int)
    log = Signal(str)
    finished = Signal()

    def __init__(self, folder, modo_lote=False, expediente_inicial=None, force_ocr=False):
        super().__init__()
        self.folder = folder
        self.modo_lote = modo_lote
        self.expediente_inicial = expediente_inicial
        self.force_ocr = force_ocr

    def run(self):
        try:
            if self.modo_lote:
                self.log.emit("Modo lote activado")
                procesar_lote(
                    self.folder,
                    expediente_inicial=self.expediente_inicial,
                    gui_log_callback=self.log.emit,
                    gui_progress_callback=self.progress.emit
                )
            else:
                self.log.emit("Modo carpeta individual activado")
                procesar_carpeta(
                    self.folder,
                    gui_log_callback=self.log.emit,
                    gui_progress_callback=self.progress.emit,
                    force_ocr=self.force_ocr
                )

            self.log.emit("✔ Finalizado")

        except Exception as e:
            self.log.emit(f"Error: {e}")

        self.finished.emit()


