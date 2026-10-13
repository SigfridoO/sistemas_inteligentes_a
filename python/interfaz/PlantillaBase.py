from PyQt6.QtWidgets import QApplication, QMainWindow

import sys

class Ventana(QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(300, 250)
        self.setWindowTitle("Mi ventana")

app = QApplication(sys.argv)
ventana = Ventana()
ventana.show()
sys.exit(app.exec())