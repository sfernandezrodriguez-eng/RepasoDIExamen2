import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QGridLayout, QLabel, QLineEdit, QCheckBox, QRadioButton,
                             QDial, QPushButton, QComboBox, QStackedLayout, QTableView, QMessageBox)
from modeloTabla import ModeloTabla


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulacro Completo de Examen")
        self.setMinimumSize(720, 480)

        # 1. LAYOUT GENERAL
        layout_general = QVBoxLayout()

        self.combo = QComboBox()
        self.combo.addItems(["Zoa 1", "Zoa 2", "Consola"])
        layout_general.addWidget(self.combo)

        # Memoria independiente para que Zoa 1 y Zoa 2 recuerden sus datos al cambiar
        self.memoria_zonas = {
            "Zoa 1": {"activa": False, "hora": "", "duracion": 0, "diario": False, "semanal": False,
                      "antixiada": False, "chuvia": False, "dias": [False]*7, "granjero": "", "genero": ""},
            "Zoa 2": {"activa": False, "hora": "", "duracion": 0, "diario": False, "semanal": False,
                      "antixiada": False, "chuvia": False, "dias": [False]*7, "granjero": "", "genero": ""}
        }
        self.zona_actual = "Zoa 1"

        # ==========================================
        # PANTALLA 0: FORMULARIO (Compartido por Zoa 1 y Zoa 2)
        # ==========================================
        grid_form = QGridLayout()

        # Fila 0: Activada y título Opcións
        grid_form.addWidget(QLabel("Zoa activada"), 0, 0)
        self.chk_activada = QCheckBox()
        grid_form.addWidget(self.chk_activada, 0, 1)
        grid_form.addWidget(QLabel("Opcións"), 0, 2)

        # Fila 1: Hora + Panel vertical de opciones
        grid_form.addWidget(QLabel("Hora de comezo (hh:mm)"), 1, 0)
        self.txt_hora = QLineEdit()
        self.txt_hora.setPlaceholderText("08:30")
        grid_form.addWidget(self.txt_hora, 1, 1)

        layout_opcions = QVBoxLayout()
        self.rad_diario = QRadioButton("Diario")
        self.rad_semanal = QRadioButton("Semanal")
        self.chk_antixiada = QCheckBox("Antixiada")
        self.chk_chuvia = QCheckBox("Chuvia")
        for w in [self.rad_diario, self.rad_semanal, self.chk_antixiada, self.chk_chuvia]:
            layout_opcions.addWidget(w)
        grid_form.addLayout(layout_opcions, 1, 2, 2, 1)

        # Fila 2: Duración + Dial
        self.lbl_duracion = QLabel("Duración rego: 0 min")
        grid_form.addWidget(self.lbl_duracion, 2, 0)
        self.dial = QDial()
        self.dial.setRange(0, 400)
        grid_form.addWidget(self.dial, 2, 1)

        # Fila 3 y 4: Días de la semana
        grid_form.addWidget(QLabel("Días"), 3, 0)
        layout_dias = QHBoxLayout()
        nombres_dias = ["Luns", "Martes", "Mércores", "Xoves", "Venres", "Sábado", "Domingo"]
        self.lista_dias = []
        for nombre in nombres_dias:
            chk = QCheckBox(nombre)
            self.lista_dias.append(chk)
            layout_dias.addWidget(chk)
        grid_form.addLayout(layout_dias, 4, 0, 1, 3)

        # Fila 5: Granjero (Nombre)
        grid_form.addWidget(QLabel("Granjero (Nombre)"), 5, 0)
        self.txt_granjero = QLineEdit()
        self.txt_granjero.setPlaceholderText("Nombre del responsable")
        grid_form.addWidget(self.txt_granjero, 5, 1)

        # Fila 6: Género (Obligatorio) + Botón Aceptar
        grid_form.addWidget(QLabel("Género"), 6, 0)
        layout_genero = QHBoxLayout()
        self.rad_home = QRadioButton("Home")
        self.rad_muller = QRadioButton("Muller")
        layout_genero.addWidget(self.rad_home)
        layout_genero.addWidget(self.rad_muller)
        grid_form.addLayout(layout_genero, 6, 1)

        self.btn_aceptar = QPushButton("Aceptar")
        grid_form.addWidget(self.btn_aceptar, 6, 2)

        pantalla_form = QWidget()
        pantalla_form.setLayout(grid_form)

        # ==========================================
        # PANTALLA 1: CONSOLA (Buscador + Tabla + Botones + Totales)
        # ==========================================
        layout_consola = QVBoxLayout()

        # Buscador superior
        layout_busqueda = QHBoxLayout()
        layout_busqueda.addWidget(QLabel("Filtrar por granjero:"))
        self.txt_buscar = QLineEdit()
        self.txt_buscar.setPlaceholderText("Escribe un nombre para filtrar...")
        layout_busqueda.addWidget(self.txt_buscar)
        layout_consola.addLayout(layout_busqueda)

        # Datos maestros iniciales
        self.datos_maestros = [
            ["Zona", "Hora", "Duración", "Activada", "Granjero", "Género", "Días", "Opcións"],
            ["Zoa 1", "08:30", "45 min", True, "Ana Perez", "Muller", "L M X", "Semanal Chuvia"],
            ["Zoa 2", "21:00", "150 min", False, "Paco Porras", "Home", "Todos", "Diario Antixiada"]
        ]

        self.modelo = ModeloTabla(list(self.datos_maestros))
        self.tvwTaboa = QTableView()
        self.tvwTaboa.setModel(self.modelo)
        layout_consola.addWidget(self.tvwTaboa)

        # Barra inferior: Totales + Botón Eliminar
        layout_pie = QHBoxLayout()
        self.lbl_totales = QLabel("Zonas activadas: 0")
        self.btn_eliminar = QPushButton("Eliminar fila seleccionada")
        layout_pie.addWidget(self.lbl_totales)
        layout_pie.addStretch()
        layout_pie.addWidget(self.btn_eliminar)
        layout_consola.addLayout(layout_pie)

        pantalla_consola = QWidget()
        pantalla_consola.setLayout(layout_consola)

        # ==========================================
        # BARAJA Y CONEXIONES
        # ==========================================
        self.baraja = QStackedLayout()
        self.baraja.addWidget(pantalla_form)     # Índice 0
        self.baraja.addWidget(pantalla_consola)  # Índice 1
        layout_general.addLayout(self.baraja)

        # Conexiones del Formulario
        self.combo.currentTextChanged.connect(self.gestionar_cambio_combo)
        self.chk_activada.stateChanged.connect(self.bloquear_controles)
        self.rad_diario.toggled.connect(self.alternar_dias)
        self.dial.valueChanged.connect(self.actualizar_dial)
        self.txt_hora.returnPressed.connect(self.comprobar_enter_hora)
        self.btn_aceptar.clicked.connect(self.guardar_registro)

        # Conexiones de la Tabla y Modelo
        self.txt_buscar.textChanged.connect(self.filtrar_tabla)
        self.btn_eliminar.clicked.connect(self.borrar_fila)
        self.tvwTaboa.clicked.connect(self.cargar_fila_en_formulario)
        self.modelo.dataChanged.connect(self.recalcular_totales)
        self.modelo.rowsInserted.connect(self.recalcular_totales)
        self.modelo.rowsRemoved.connect(self.recalcular_totales)

        # Estado inicial
        self.bloquear_controles(0)
        self.recalcular_totales()

        contenedor = QWidget()
        contenedor.setLayout(layout_general)
        self.setCentralWidget(contenedor)

    # --- LÓGICA DEL FORMULARIO ---

    def bloquear_controles(self, estado):
        activo = (estado == 2)
        widgets = [self.txt_hora, self.dial, self.rad_diario, self.rad_semanal,
                   self.chk_antixiada, self.chk_chuvia, self.txt_granjero,
                   self.rad_home, self.rad_muller, self.btn_aceptar]
        for w in widgets:
            w.setEnabled(activo)

        # Los días solo se activan si la zona está activa Y no está marcado "Diario"
        for chk in self.lista_dias:
            chk.setEnabled(activo and not self.rad_diario.isChecked())

    def alternar_dias(self, es_diario):
        if self.chk_activada.isChecked():
            for chk in self.lista_dias:
                chk.setEnabled(not es_diario)
                if es_diario:
                    chk.setChecked(False)

    def actualizar_dial(self, valor):
        self.lbl_duracion.setText(f"Duración rego: {valor} min")

    def es_hora_valida(self, texto):
        if len(texto) != 5 or texto[2] != ":":
            return False
        try:
            h, m = int(texto[:2]), int(texto[3:])
            return 0 <= h <= 23 and 0 <= m <= 59
        except ValueError:
            return False

    def comprobar_enter_hora(self):
        if self.es_hora_valida(self.txt_hora.text()):
            self.txt_hora.setStyleSheet("background-color: lightgreen;")
        else:
            self.txt_hora.setStyleSheet("background-color: #ffcccc;")

    def gestionar_cambio_combo(self, nueva_opcion):
        # Guardar estado de la zona anterior en memoria
        if self.zona_actual in self.memoria_zonas:
            self.memoria_zonas[self.zona_actual] = {
                "activa": self.chk_activada.isChecked(),
                "hora": self.txt_hora.text(),
                "duracion": self.dial.value(),
                "diario": self.rad_diario.isChecked(),
                "semanal": self.rad_semanal.isChecked(),
                "antixiada": self.chk_antixiada.isChecked(),
                "chuvia": self.chk_chuvia.isChecked(),
                "dias": [chk.isChecked() for chk in self.lista_dias],
                "granjero": self.txt_granjero.text(),
                "genero": "Home" if self.rad_home.isChecked() else ("Muller" if self.rad_muller.isChecked() else "")
            }

        if nueva_opcion == "Consola":
            self.baraja.setCurrentIndex(1)
        else:
            self.baraja.setCurrentIndex(0)
            self.zona_actual = nueva_opcion
            d = self.memoria_zonas[nueva_opcion]
            self.chk_activada.setChecked(d["activa"])
            self.txt_hora.setText(d["hora"])
            self.dial.setValue(d["duracion"])
            self.rad_diario.setChecked(d["diario"])
            self.rad_semanal.setChecked(d["semanal"])
            self.chk_antixiada.setChecked(d["antixiada"])
            self.chk_chuvia.setChecked(d["chuvia"])
            for chk, marcado in zip(self.lista_dias, d["dias"]):
                chk.setChecked(marcado)
            self.txt_granjero.setText(d["granjero"])
            self.rad_home.setChecked(d["genero"] == "Home")
            self.rad_muller.setChecked(d["genero"] == "Muller")

    def guardar_registro(self):
        hora = self.txt_hora.text()
        nombre = self.txt_granjero.text().strip()

        # Validaciones
        if not self.es_hora_valida(hora):
            self.txt_hora.setStyleSheet("background-color: #ffcccc;")
            QMessageBox.warning(self, "Error", "Formato de hora inválido (debe ser hh:mm).")
            return
        self.txt_hora.setStyleSheet("")

        if nombre == "":
            self.txt_granjero.setStyleSheet("background-color: #ffcccc;")
            QMessageBox.warning(self, "Error", "Debes indicar el nombre del granjero.")
            return
        self.txt_granjero.setStyleSheet("")

        if self.rad_home.isChecked():
            genero = "Home"
        elif self.rad_muller.isChecked():
            genero = "Muller"
        else:
            QMessageBox.warning(self, "Error", "Es obligatorio seleccionar un género.")
            return

        # Recoger días y opciones
        dias_txt = "Todos" if self.rad_diario.isChecked() else " ".join(
            [chk.text()[:2] for chk in self.lista_dias if chk.isChecked()]
        )
        opcions = []
        if self.rad_diario.isChecked(): opcions.append("Diario")
        if self.rad_semanal.isChecked(): opcions.append("Semanal")
        if self.chk_antixiada.isChecked(): opcions.append("Antixiada")
        if self.chk_chuvia.isChecked(): opcions.append("Chuvia")

        nova_fila = [
            self.zona_actual,
            hora,
            f"{self.dial.value()} min",
            self.chk_activada.isChecked(),
            nombre.capitalize(),
            genero,
            dias_txt if dias_txt != "" else "Ninguno",
            " ".join(opcions)
        ]

        # Guardar tanto en la copia maestra (para el filtro) como en el modelo
        self.datos_maestros.append(nova_fila)
        self.txt_buscar.clear()  # Limpiar filtro para que se vea la nueva fila
        self.modelo.engadirFila(nova_fila)
        self.combo.setCurrentText("Consola")

    # --- LÓGICA DE LA TABLA ---

    def filtrar_tabla(self, texto):
        filtradas = [self.datos_maestros[0]]
        for fila in self.datos_maestros[1:]:
            if texto.lower() in fila[4].lower():
                filtradas.append(fila)
        self.modelo.tabla = filtradas
        self.modelo.layoutChanged.emit()
        self.recalcular_totales()

    def borrar_fila(self):
        fila_sel = self.tvwTaboa.currentIndex().row()
        if fila_sel != -1:
            fila_datos = self.modelo.tabla[fila_sel + 1]
            if fila_datos in self.datos_maestros:
                self.datos_maestros.remove(fila_datos)
            self.modelo.eliminarFila(fila_sel)

    def cargar_fila_en_formulario(self, indice):
        # Si hacen clic en una fila, cargamos sus datos básicos en la zona correspondiente
        fila = self.modelo.tabla[indice.row() + 1]
        zona = fila[0]
        if zona in self.memoria_zonas:
            self.memoria_zonas[zona]["activa"] = fila[3]
            self.memoria_zonas[zona]["hora"] = fila[1]
            self.memoria_zonas[zona]["duracion"] = int(fila[2].replace(" min", ""))
            self.memoria_zonas[zona]["granjero"] = fila[4]
            self.memoria_zonas[zona]["genero"] = fila[5]

    def recalcular_totales(self):
        activas = sum(1 for fila in self.modelo.tabla[1:] if fila[3] is True)
        self.lbl_totales.setText(f"Zonas activadas visibles: {activas}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VentanaPrincipal()
    window.show()
    sys.exit(app.exec())