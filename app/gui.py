import os
from pathlib import Path

from PySide6.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog,
    QProgressBar, QTextEdit, QMessageBox, QCheckBox, QLineEdit
)
from PySide6.QtCore import Qt, QThread

from app.worker import Worker


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
                self.setStyleSheet(f.read())
        else:
            print(" No se encontró el archivo QSS, usando estilo por defecto.")

    # -------------------------------------------
    # UI
    # -------------------------------------------
    def setup_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Selecciona una carpeta...")
        self.label.setAlignment(Qt.AlignCenter)

        self.btn_select = QPushButton("Seleccionar carpeta")
        self.btn_select.clicked.connect(self.select_folder)

        # Modo lote
        self.chk_lote = QCheckBox("Modo lote (procesar subcarpetas)")

        self.input_exp = QLineEdit()
        self.input_exp.setPlaceholderText("Expediente inicial (solo lote)")
        self.input_exp.setEnabled(False)

        self.chk_lote.stateChanged.connect(
            lambda: self.input_exp.setEnabled(self.chk_lote.isChecked())
        )

        self.btn_process = QPushButton("Procesar")
        self.btn_process.clicked.connect(self.process_folder)
        self.btn_process.setEnabled(False)

        self.progress = QProgressBar()
        self.progress.setValue(0)

        self.log = QTextEdit()
        self.log.setReadOnly(True)

        self.btn_open_output = QPushButton("Abrir carpeta output")
        self.btn_open_output.clicked.connect(self.open_output)

        # Añadir widgets al layout
        layout.addWidget(self.label)
        layout.addWidget(self.btn_select)
        layout.addWidget(self.chk_lote)
        layout.addWidget(self.input_exp)
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
    # Procesar carpeta usando Worker
    # -------------------------------------------
    def process_folder(self):
        if not hasattr(self, "folder"):
            QMessageBox.warning(self, "Error", "No se ha seleccionado ninguna carpeta.")
            return

        modo_lote = self.chk_lote.isChecked()
        expediente = None

        if modo_lote:
            if not self.input_exp.text().isdigit():
                QMessageBox.warning(self, "Error", "Debes ingresar un número de expediente inicial.")
                return
            expediente = int(self.input_exp.text())

        # Thread
        self.thread = QThread()
        self.worker = Worker(self.folder, modo_lote=modo_lote, expediente_inicial=expediente)

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.log.connect(self.append_log)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    # -------------------------------------------
    # Mostrar logs
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


# Para ejecución directa
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
