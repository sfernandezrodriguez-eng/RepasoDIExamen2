import sys
# 1. Importar QCheckBox
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QCheckBox

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi App")

        # --- AQUÍ VAN TUS LAYOUTS Y WIDGETS ---
        layout_principal = QVBoxLayout()

        # 2. Crear el QCheckBox
        self.mi_checkbox = QCheckBox("Aceptar condiciones")
        self.mi_checkbox2 = QCheckBox("Aceptar condiciones otra vez")

        # 3. Añadirlo al layout
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