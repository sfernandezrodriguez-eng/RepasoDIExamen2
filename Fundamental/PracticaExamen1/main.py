import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QGridLayout, QLabel, QLineEdit, QCheckBox, QRadioButton,
                             QDial, QPushButton, QComboBox, QStackedLayout, QTableView, QMessageBox)
from modeloTabla import ModeloTabla


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Examen Unido: Riego + Granjeros + Tabla")
        self.setMinimumSize(620, 400)

        # 1. LAYOUT PRINCIPAL
        layout_principal = QVBoxLayout()

        self.combo = QComboBox()
        self.combo.addItems(["Configuración Zoa 1", "Consola (Tabla)"])
        layout_principal.addWidget(self.combo)

        # ==========================================
        # PANTALLA 1: FORMULARIO
        # ==========================================
        grid_form = QGridLayout()

        # Fila 0: Activada
        grid_form.addWidget(QLabel("Zoa activada:"), 0, 0)
        self.chk_activar = QCheckBox()
        grid_form.addWidget(self.chk_activar, 0, 1)

        # Fila 1: Hora
        grid_form.addWidget(QLabel("Hora (hh:mm):"), 1, 0)
        self.txt_hora = QLineEdit()
        self.txt_hora.setPlaceholderText("Ej: 08:30")
        grid_form.addWidget(self.txt_hora, 1, 1)

        # Fila 2: Duración
        self.lbl_duracion = QLabel("Duración: 0")
        grid_form.addWidget(self.lbl_duracion, 2, 0)
        self.dial = QDial()
        self.dial.setRange(0, 400)
        grid_form.addWidget(self.dial, 2, 1)

        # Fila 3: Granjero (Nombre)
        grid_form.addWidget(QLabel("Granjero (Nombre):"), 3, 0)
        self.txt_granjero = QLineEdit()
        self.txt_granjero.setPlaceholderText("Introduce nombre")
        grid_form.addWidget(self.txt_granjero, 3, 1)

        # Fila 4: Género del Granjero (RadioButtons obligatorios)
        grid_form.addWidget(QLabel("Género:"), 4, 0)
        layout_genero = QHBoxLayout()
        self.rad_home = QRadioButton("Home")
        self.rad_muller = QRadioButton("Muller")
        layout_genero.addWidget(self.rad_home)
        layout_genero.addWidget(self.rad_muller)
        grid_form.addLayout(layout_genero, 4, 1)

        # Fila 5: Botón Aceptar
        self.btn_aceptar = QPushButton("Aceptar")
        grid_form.addWidget(self.btn_aceptar, 5, 1)

        pantalla_form = QWidget()
        pantalla_form.setLayout(grid_form)

        # ==========================================
        # PANTALLA 2: TABLA (Consola)
        # ==========================================
        layout_tabla = QVBoxLayout()

        datos = [
            ["Zona", "Hora", "Duración", "Activada", "Granjero", "Género"],
            ["Zona 1", "08:30", "45 min", True, "Ana Perez", "Muller"],
            ["Zona 2", "21:00", "120 min", False, "Paco Porras", "Home"]
        ]

        self.modelo = ModeloTabla(datos)
        self.tvwTaboa = QTableView()
        self.tvwTaboa.setModel(self.modelo)
        layout_tabla.addWidget(self.tvwTaboa)

        pantalla_tabla = QWidget()
        pantalla_tabla.setLayout(layout_tabla)

        # ==========================================
        # BARAJA Y CONEXIONES
        # ==========================================
        self.baraja = QStackedLayout()
        self.baraja.addWidget(pantalla_form)   # Índice 0
        self.baraja.addWidget(pantalla_tabla)  # Índice 1
        layout_principal.addLayout(self.baraja)

        self.combo.currentIndexChanged.connect(self.baraja.setCurrentIndex)
        self.chk_activar.stateChanged.connect(self.bloquear_controles)
        self.dial.valueChanged.connect(self.actualizar_dial)
        self.txt_hora.returnPressed.connect(self.comprobar_enter_hora)
        self.btn_aceptar.clicked.connect(self.guardar_en_tabla)

        # Arrancar con controles bloqueados hasta marcar el checkbox
        self.bloquear_controles(0)

        contenedor = QWidget()
        contenedor.setLayout(layout_principal)
        self.setCentralWidget(contenedor)

    # --- LÓGICA Y VALIDACIONES ---

    def bloquear_controles(self, estado):
        activo = (estado == 2)
        self.txt_hora.setEnabled(activo)
        self.dial.setEnabled(activo)
        self.txt_granjero.setEnabled(activo)
        self.rad_home.setEnabled(activo)
        self.rad_muller.setEnabled(activo)
        self.btn_aceptar.setEnabled(activo)

    def actualizar_dial(self, valor):
        self.lbl_duracion.setText(f"Duración: {valor}")

    def es_hora_valida(self, texto):
        if len(texto) != 5 or texto[2] != ":":
            return False
        try:
            horas = int(texto[:2])
            minutos = int(texto[3:])
            return 0 <= horas <= 23 and 0 <= minutos <= 59
        except ValueError:
            return False

    def comprobar_enter_hora(self):
        hora = self.txt_hora.text()
        if self.es_hora_valida(hora):
            self.txt_hora.setStyleSheet("background-color: lightgreen;")
        else:
            self.txt_hora.setStyleSheet("background-color: #ffcccc;")

    def guardar_en_tabla(self):
        hora = self.txt_hora.text()
        nombre = self.txt_granjero.text().strip()

        # 1. Validar Hora (hh:mm)
        if not self.es_hora_valida(hora):
            self.txt_hora.setStyleSheet("background-color: #ffcccc;")
            QMessageBox.warning(self, "Error", "La hora debe tener el formato válido hh:mm (00:00 - 23:59).")
            return
        self.txt_hora.setStyleSheet("")

        # 2. Validar Nombre del Granjero
        if nombre == "":
            self.txt_granjero.setStyleSheet("background-color: #ffcccc;")
            QMessageBox.warning(self, "Error", "Debes escribir el nombre del granjero.")
            return
        self.txt_granjero.setStyleSheet("")

        # 3. Validar Género obligatorio (no puede no tener género)
        if self.rad_home.isChecked():
            genero = "Home"
        elif self.rad_muller.isChecked():
            genero = "Muller"
        else:
            QMessageBox.warning(self, "Error", "Es obligatorio seleccionar un género (Home o Muller).")
            return

        # 4. Guardar fila y cambiar a la vista de la tabla
        zona = "Zona 1"
        duracion = f"{self.dial.value()} min"
        activada = self.chk_activar.isChecked()

        self.modelo.engadirFila([zona, hora, duracion, activada, nombre.capitalize(), genero])
        self.combo.setCurrentIndex(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VentanaPrincipal()
    window.show()
    sys.exit(app.exec())