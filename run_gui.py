from app.gui import MainWindow
from PySide6.QtWidgets import QApplication
import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
