from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt

import sys
from pathlib import Path

def abs_path(nombre_archivo):
    return str(  Path(__file__).parent / nombre_archivo)

class Ventana(QMainWindow):

    def __init__(self):
        super().__init__()

        mi_etiqueta = QLabel("Saludos")
        mi_etiqueta.setAlignment(Qt.AlignmentFlag.AlignTop |
                                 Qt.AlignmentFlag.AlignRight)

        fuente = QFont("Manjari", 20, QFont.Weight.Bold, italic=True)
        mi_etiqueta.setFont(fuente)
        ruta = abs_path("aves-exoticas.jpg")
        print(ruta)
        imagen = QPixmap(ruta)
        mi_etiqueta.setPixmap(imagen)
        mi_etiqueta.setScaledContents(True)
        self.setCentralWidget(mi_etiqueta)

        self.resize(300, 70)
        self.setWindowTitle("Mi ventana")

app = QApplication(sys.argv)
ventana = Ventana()
ventana.show()
sys.exit(app.exec())