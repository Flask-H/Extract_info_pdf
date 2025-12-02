import os
from PySide6.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout,
    QFileDialog, QProgressBar, QTextEdit, QMessageBox
)
from PySide6.QtCore import Qt, QThread
from pathlib import Path

from app.worker import Worker  # Nuestro worker que procesa carpetas


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Extract Info PDF — Automatización")
        self.resize(600, 450)

        self.setup_ui()
        self.apply_stylesheet()

    # -------------------------------------------
    # Cargar estilos .QSS
    # -------------------------------------------
    def apply_stylesheet(self):
        qss_file = Path(__file__).parent / "styles" / "dark_theme.qss"

        if qss_file.exists():
            with open(qss_file, "r", encoding="utf-8") as f:
                style = f.read()
                self.setStyleSheet(style)
        else:
            print(" No se encontró el archivo QSS, usando estilo por defecto.")

    # -------------------------------------------
    # UI
    # -------------------------------------------
    def setup_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Selecciona una carpeta con documentos PDF/DOCX")
        self.label.setAlignment(Qt.AlignCenter)

        self.btn_select = QPushButton("Seleccionar carpeta")
        self.btn_select.clicked.connect(self.select_folder)

        self.btn_process = QPushButton("Procesar")
        self.btn_process.clicked.connect(self.process_folder)
        self.btn_process.setEnabled(False)

        self.progress = QProgressBar()
        self.progress.setValue(0)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setPlaceholderText("Log del sistema...")

        self.btn_open_output = QPushButton("Abrir carpeta output")
        self.btn_open_output.clicked.connect(self.open_output)

        layout.addWidget(self.label)
        layout.addWidget(self.btn_select)
        layout.addWidget(self.btn_process)
        layout.addWidget(self.progress)
        layout.addWidget(self.log)
        layout.addWidget(self.btn_open_output)

        self.setLayout(layout)

    # -------------------------------------------
    # Seleccionar carpeta
    # -------------------------------------------
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta")
        if folder:
            self.folder = Path(folder)
            self.label.setText(f"Carpeta seleccionada:\n{folder}")
            self.btn_process.setEnabled(True)

    # -------------------------------------------
    # Procesar carpeta con Worker
    # -------------------------------------------
    def process_folder(self):
        if not hasattr(self, "folder"):
            QMessageBox.warning(self, "Error", "No se ha seleccionado ninguna carpeta.")
            return

        self.thread = QThread()
        self.worker = Worker(self.folder)

        self.worker.moveToThread(self.thread)

        # Eventos del worker
        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.log.connect(self.append_log)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    # -------------------------------------------
    # Mostrar logs en pantalla
    # -------------------------------------------
    def append_log(self, msg):
        self.log.append(msg)

    # -------------------------------------------
    # Abrir carpeta output
    # -------------------------------------------
    def open_output(self):
        output = Path("C:/Users/Usuario/Documents/Proyecto_Output/")
        output.mkdir(exist_ok=True)
        os.startfile(output)

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())