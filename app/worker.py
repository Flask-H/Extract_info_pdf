from PySide6.QtCore import QObject, Signal
from main import procesar_carpeta


class Worker(QObject):
    progress = Signal(int)
    log = Signal(str)
    finished = Signal()

    def __init__(self, folder):
        super().__init__()
        self.folder = folder

    def run(self):
        try:
            self.log.emit(f"Procesando carpeta: {self.folder}")
            procesar_carpeta(
                self.folder,
                gui_log_callback=self.log.emit,
                gui_progress_callback=self.progress.emit
            )
            self.log.emit("✔ Finalizado")
        except Exception as e:
            self.log.emit(f" Error: {e}")

        self.finished.emit()
