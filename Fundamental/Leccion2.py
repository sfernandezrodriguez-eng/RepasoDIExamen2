import sys
# 1. Cambiamos QVBoxLayout por QHBoxLayout
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QCheckBox

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi App")

        # 2. Usamos QHBoxLayout para que los coloque en fila (horizontal)
        layout_principal = QHBoxLayout()

        # Crear los QCheckBox
        self.mi_checkbox = QCheckBox("Aceptar condiciones")
        self.mi_checkbox2 = QCheckBox("Aceptar condiciones otra vez")

        # Añadirlos al layout
        layout_principal.addWidget(self.mi_checkbox)
        layout_principal.addWidget(self.mi_checkbox2)

        # OBLIGATORIO en QMainWindow: widget central
        contenedor = QWidget()
        contenedor.setLayout(layout_principal)
        self.setCentralWidget(contenedor)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VentanaPrincipal()
    window.show()
    sys.exit(app.exec())