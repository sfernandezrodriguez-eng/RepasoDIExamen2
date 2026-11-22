import sys
# 1. Cambiamos QVBoxLayout por QHBoxLayout
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QCheckBox, QVBoxLayout


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi App")

        # 2. Usamos QHBoxLayout para que los coloque en fila (horizontal)
        layout_principal = QHBoxLayout()

        columna_izquierda = QVBoxLayout()

        # Crear los QCheckBox
        self.mi_checkbox = QCheckBox("Aceptar condiciones")
        self.mi_checkbox2 = QCheckBox("Aceptar condiciones otra vez")
        self.mi_checkbox3 = QCheckBox("Aceptar condiciones otra vez")

        columna_izquierda.addWidget(self.mi_checkbox)
        columna_izquierda.addWidget(self.mi_checkbox3)


        # Añadirlos al layout

        layout_principal.addLayout(columna_izquierda)
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