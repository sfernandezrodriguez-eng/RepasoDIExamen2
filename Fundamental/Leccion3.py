import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QCheckBox

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi App")

        # Cambiamos a QGridLayout (cuadrícula)
        layout_principal = QGridLayout()

        self.mi_checkbox = QCheckBox("Aceptar condiciones")
        self.mi_checkbox2 = QCheckBox("Aceptar condiciones otra vez")
        self.mi_checkbox3 = QCheckBox("Debajo del primero")

        # addWidget(widget, fila, columna)
        layout_principal.addWidget(self.mi_checkbox, 0, 0)   # Fila 0, Col 0
        layout_principal.addWidget(self.mi_checkbox2, 0, 1)  # Fila 0, Col 1 (a la derecha del 1)
        layout_principal.addWidget(self.mi_checkbox3, 1, 0)  # Fila 1, Col 0 (debajo del 1)

        contenedor = QWidget()
        contenedor.setLayout(layout_principal)
        self.setCentralWidget(contenedor)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VentanaPrincipal()
    window.show()
    sys.exit(app.exec())