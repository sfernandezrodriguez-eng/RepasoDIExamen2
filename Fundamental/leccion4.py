import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QCheckBox, QPushButton, QComboBox, QStackedLayout)


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ejemplo ComboBox + Layouts")

        # 1. LAYOUT PRINCIPAL (Vertical: arriba el ComboBox, abajo las pantallas)
        layout_principal = QVBoxLayout()

        # Crear el desplegable
        self.combo = QComboBox()
        self.combo.addItems(["Pantalla Checkboxes", "Pantalla Botones"])
        layout_principal.addWidget(self.combo)

        # 2. PANTALLA 1 (Layout vertical dentro de un QWidget)
        layout_pantalla1 = QVBoxLayout()
        layout_pantalla1.addWidget(QCheckBox("Opción A"))
        layout_pantalla1.addWidget(QCheckBox("Opción B"))

        pantalla1 = QWidget()
        pantalla1.setLayout(layout_pantalla1)

        # 3. PANTALLA 2 (Layout horizontal dentro de otro QWidget)
        layout_pantalla2 = QHBoxLayout()
        layout_pantalla2.addWidget(QPushButton("Botón 1"))
        layout_pantalla2.addWidget(QPushButton("Botón 2"))

        pantalla2 = QWidget()
        pantalla2.setLayout(layout_pantalla2)

        # 4. BARAJA DE PANTALLAS (Apila los QWidget uno encima de otro)
        self.baraja = QStackedLayout()
        self.baraja.addWidget(pantalla1)  # Índice 0
        self.baraja.addWidget(pantalla2)  # Índice 1

        layout_principal.addLayout(self.baraja)

        # 5. CONECTAR EL COMBOBOX CON LA BARAJA
        self.combo.currentIndexChanged.connect(self.baraja.setCurrentIndex)

        # OBLIGATORIO en QMainWindow: widget central
        contenedor = QWidget()
        contenedor.setLayout(layout_principal)
        self.setCentralWidget(contenedor)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VentanaPrincipal()
    window.show()
    sys.exit(app.exec())