import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QGridLayout, QLabel, QLineEdit, QCheckBox,
                             QDial, QPushButton, QComboBox, QStackedLayout, QTextEdit)


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ejemplo Intermedio")

        # 1. LAYOUT PRINCIPAL (Combo arriba, baraja abajo)
        layout_principal = QVBoxLayout()

        self.combo = QComboBox()
        self.combo.addItems(["Configuración", "Consola"])
        layout_principal.addWidget(self.combo)

        # ==========================================
        # PANTALLA 1: FORMULARIO (QGridLayout)
        # ==========================================
        grid_form = QGridLayout()

        grid_form.addWidget(QLabel("Activar zona:"), 0, 0)
        self.chk_activar = QCheckBox()
        grid_form.addWidget(self.chk_activar, 0, 1)

        grid_form.addWidget(QLabel("Hora (hh:mm):"), 1, 0)
        self.txt_hora = QLineEdit()
        grid_form.addWidget(self.txt_hora, 1, 1)

        self.lbl_duracion = QLabel("Duración: 0")
        grid_form.addWidget(self.lbl_duracion, 2, 0)
        self.dial = QDial()
        self.dial.setRange(0, 100)
        grid_form.addWidget(self.dial, 2, 1)

        self.btn_aceptar = QPushButton("Aceptar")
        grid_form.addWidget(self.btn_aceptar, 3, 1)

        pantalla_form = QWidget()
        pantalla_form.setLayout(grid_form)

        # ==========================================
        # PANTALLA 2: CONSOLA (QTextEdit)
        # ==========================================
        layout_consola = QVBoxLayout()
        self.consola = QTextEdit()
        layout_consola.addWidget(self.consola)

        pantalla_consola = QWidget()
        pantalla_consola.setLayout(layout_consola)

        # ==========================================
        # BARAJA Y CONEXIONES
        # ==========================================
        self.baraja = QStackedLayout()
        self.baraja.addWidget(pantalla_form)    # Índice 0
        self.baraja.addWidget(pantalla_consola) # Índice 1
        layout_principal.addLayout(self.baraja)

        # Conectar señales
        self.combo.currentIndexChanged.connect(self.baraja.setCurrentIndex)
        self.chk_activar.stateChanged.connect(self.bloquear_controles)
        self.dial.valueChanged.connect(self.actualizar_dial)
        self.btn_aceptar.clicked.connect(self.enviar_a_consola)

        # Arrancar con los controles bloqueados (porque el check empieza desmarcado)
        self.bloquear_controles(0)

        # Widget central obligatorio
        contenedor = QWidget()
        contenedor.setLayout(layout_principal)
        self.setCentralWidget(contenedor)

    # --- FUNCIONES DE LÓGICA ---

    def bloquear_controles(self, estado):
        # Si estado == 2 (marcado), activo es True; si no, False
        activo = (estado == 2)
        self.txt_hora.setEnabled(activo)
        self.dial.setEnabled(activo)
        self.btn_aceptar.setEnabled(activo)

    def actualizar_dial(self, valor):
        self.lbl_duracion.setText(f"Duración: {valor}")

    def enviar_a_consola(self):
        hora = self.txt_hora.text()
        duracion = self.dial.value()
        # Añadir línea sin borrar lo anterior
        self.consola.append(f"Hora: {hora} | Duración: {duracion} min")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VentanaPrincipal()
    window.show()
    sys.exit(app.exec())