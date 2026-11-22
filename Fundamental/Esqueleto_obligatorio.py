import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi App")

        # --- AQUÍ VAN TUS LAYOUTS Y WIDGETS ---
        layout_principal = QVBoxLayout()

        # OBLIGATORIO en QMainWindow: widget central
        contenedor = QWidget()
        contenedor.setLayout(layout_principal)
        self.setCentralWidget(contenedor)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VentanaPrincipal()
    window.show()
    sys.exit(app.exec())