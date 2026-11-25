import sys
import math

# 1. IMPORTACIONES: Traemos todas las piezas visuales (widgets) que vamos a usar
from PyQt6.QtWidgets import (QMainWindow, QApplication, QVBoxLayout, QPushButton, QWidget, QLabel, QLineEdit,
                             QHBoxLayout, QListView, QRadioButton, QComboBox, QGridLayout, QStackedLayout, QCheckBox,
                             QDial, QTextEdit, QAbstractSlider)
from PyQt6.QtGui import QColor, QPalette


# 2. LA VENTANA PRINCIPAL: Heredamos de QMainWindow para crear nuestra ventana
class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()  # Arranca la ventana base de Qt
        self.setWindowTitle("ExamenA")  # Título de arriba de la ventana

        # Límites de tamaño (mínimo 100x100 px, máximo 1000x1000 px)
        self.setMinimumSize(100, 100)
        self.setMaximumSize(1000, 1000)

        # 'maia' es el organizador principal de toda la ventana (apila cosas de arriba a abajo)
        maia = QVBoxLayout()

        # DESPLEGABLE SUPERIOR (Para cambiar entre las 3 pantallas)
        self.selec = QComboBox()
        self.selec.addItems(["Configuración zoa 1", "Zoa 2", "Consola"])  # Opciones: índice 0, 1 y 2
        self.selec.setCurrentIndex(0)  # Empieza seleccionando la primera opción ("Configuración zoa 1")

        # Metemos el desplegable arriba del todo en el organizador principal
        maia.addWidget(self.selec)

        # =========================================================================
        # PANTALLA 0: CONFIGURACIÓN (Formulario principal)
        # =========================================================================
        conf = QWidget()  # Caja vacía que contendrá toda esta pantalla
        pantalla_conf = QGridLayout()  # Organizador tipo tabla de Excel (filas y columnas)

        # --- Fila 0 ---
        self.activada = QLabel("Activada")  # Texto fijo
        pantalla_conf.addWidget(self.activada, 0, 0)  # Fila 0, Columna 0

        self.checkbox = QCheckBox()  # Casilla para marcar/desmarcar (enciende o apaga el formulario)
        pantalla_conf.addWidget(self.checkbox, 0, 1)  # Fila 0, Columna 1

        self.opcions = QLabel("Opcions")  # Texto fijo
        pantalla_conf.addWidget(self.opcions, 0, 2)  # Fila 0, Columna 2

        # --- Fila 1 ---
        self.hora_rego = QLabel("Hora de comenzo do rego")
        pantalla_conf.addWidget(self.hora_rego, 1, 0)  # Fila 1, Columna 0

        self.text = QLineEdit()  # Caja de texto de una línea para escribir la hora (ej: "14:30")
        pantalla_conf.addWidget(self.text, 1, 1)  # Fila 1, Columna 1

        # Sub-organizador vertical para apilar los botones de la derecha
        vertical = QVBoxLayout()
        self.diario = QRadioButton("Diario")      # Botón redondo (solo se puede elegir uno)
        self.semanal = QRadioButton("Semanal")    # Botón redondo
        self.antixiada = QCheckBox("Antixiada")   # Casilla cuadrada (se pueden marcar varias)
        self.chuvia = QCheckBox("Chuvia")         # Casilla cuadrada

        # Metemos los 4 botones dentro del sub-organizador vertical
        vertical.addWidget(self.diario)
        vertical.addWidget(self.semanal)
        vertical.addWidget(self.antixiada)
        vertical.addWidget(self.chuvia)

        # Metemos ese bloque vertical en la tabla: Fila 1, Col 2, ocupando 1 fila y 3 columnas
        pantalla_conf.addLayout(vertical, 1, 2, 1, 3)

        # --- Fila 2 ---
        self.duracion_rego = QLabel("Duracion rego")
        pantalla_conf.addWidget(self.duracion_rego, 2, 0)  # Fila 2, Columna 0

        self.dial = QDial()  # Ruleta giratoria
        self.dial.setRange(0, 400)  # Valores posibles de la ruleta: de 0 a 400
        pantalla_conf.addWidget(self.dial, 2, 1)  # Fila 2, Columna 1

        # --- Fila 3 ---
        self.dias = QLabel("Dias")
        pantalla_conf.addWidget(self.dias, 3, 0)  # Fila 3, Columna 0

        # --- Fila 4: Los 7 días de la semana en horizontal ---
        horizontal = QHBoxLayout()  # Sub-organizador de izquierda a derecha

        self.checkboxL = QCheckBox("Lunes")
        self.checkboxM = QCheckBox("Martes")
        self.checkboxX = QCheckBox("Miercoles")
        self.checkboxJ = QCheckBox("Jueves")
        self.checkboxV = QCheckBox("Viernes")
        self.checkboxS = QCheckBox("Sabado")
        self.checkboxD = QCheckBox("Domingo")

        # Metemos los 7 checkboxes en la fila horizontal
        horizontal.addWidget(self.checkboxL)
        horizontal.addWidget(self.checkboxM)
        horizontal.addWidget(self.checkboxX)
        horizontal.addWidget(self.checkboxJ)
        horizontal.addWidget(self.checkboxV)
        horizontal.addWidget(self.checkboxS)
        horizontal.addWidget(self.checkboxD)

        # Metemos la fila horizontal en la tabla: Fila 4, Col 0, ocupando 1 fila y 3 columnas
        pantalla_conf.addLayout(horizontal, 4, 0, 1, 3)

        # --- Fila 5: Botón Aceptar ---
        self.aceptar = QPushButton("Aceptar")
        pantalla_conf.addWidget(self.aceptar, 5, 2)  # Fila 5, Columna 2

        # Cerramos la pantalla 0 metiendo la tabla 'pantalla_conf' dentro de la caja 'conf'
        conf.setLayout(pantalla_conf)

        # =========================================================================
        # CONEXIÓN DE EVENTOS (Qué pasa cuando el usuario toca cada control)
        # =========================================================================
        # 1. Al marcar/desmarcar el checkbox 'Activada', llama a activarZoa()
        self.checkbox.stateChanged.connect(self.activarZoa)
        # Llamamos manualmente a activarZoa(0) nada más arrancar para que empiece todo desactivado (gris)
        self.activarZoa(0)

        # 2. Al girar la ruleta, llama a textoRego() para actualizar el texto con el número
        self.dial.valueChanged.connect(self.textoRego)

        # 3. Al pulsar la tecla ENTER dentro de la caja de texto de la hora, llama a comporbarHora()
        self.text.returnPressed.connect(self.comporbarHora)

        # 4. Al hacer clic en 'Aceptar', llama a activarAceptar() para enviar todo a la consola
        self.aceptar.clicked.connect(self.activarAceptar)

        # =========================================================================
        # PANTALLA 1: ZOA 2 (Pantalla secundaria de ejemplo)
        # =========================================================================
        zoa = QWidget()
        pantalla_zoa = QGridLayout()
        etiqueta = QLabel("Etiqueta")
        pantalla_zoa.addWidget(etiqueta, 0, 0)
        zoa.setLayout(pantalla_zoa)

        # =========================================================================
        # PANTALLA 2: CONSOLA (Donde se imprimen los resultados y errores)
        # =========================================================================
        consola = QWidget()
        pantalla_consola = QGridLayout()
        self.texto = QTextEdit()  # Caja de texto grande multilínea
        pantalla_consola.addWidget(self.texto, 0, 0)
        consola.setLayout(pantalla_consola)

        # =========================================================================
        # BARAJA DE PANTALLAS (QStackedLayout) Y MONTAJE FINAL
        # =========================================================================
        self.tarxetas = QStackedLayout()  # Apila las 3 pantallas una encima de otra
        self.tarxetas.addWidget(conf)     # Índice 0
        self.tarxetas.addWidget(zoa)      # Índice 1
        self.tarxetas.addWidget(consola)  # Índice 2

        # Añadimos la baraja debajo del desplegable en el organizador principal
        maia.addLayout(self.tarxetas)

        # OBLIGATORIO en QMainWindow: meter el organizador principal en un QWidget central
        contenedor = QWidget()
        contenedor.setLayout(maia)
        self.setCentralWidget(contenedor)

        # Conectamos el desplegable de arriba para que cambie de pantalla al elegir otra opción
        self.selec.currentIndexChanged.connect(self.cambiarFormulario)

        # Asegura que al iniciar se muestre la pantalla 0
        self.tarxetas.setCurrentIndex(0)
        self.tarxetas.currentWidget().hide()
        self.cambiarFormulario(0)

    # =============================================================================
    # FUNCIONES (La lógica del programa)
    # =============================================================================

    # Cambia la pantalla visible según el índice elegido en el QComboBox (0, 1 o 2)
    def cambiarFormulario(self, indice):
        self.tarxetas.currentWidget().show()
        self.tarxetas.setCurrentIndex(indice)
        self.tarxetas.currentWidget().show()

    # Activa (True) o desactiva/pone en gris (False) todos los controles del formulario
    def activarZoa(self, estado):
        # En PyQt6, un QCheckBox marcado envía el número 2; desmarcado envía 0
        if estado == 2:
            self.hora_rego.setEnabled(True)
            self.text.setEnabled(True)
            self.diario.setEnabled(True)
            self.semanal.setEnabled(True)
            self.antixiada.setEnabled(True)
            self.chuvia.setEnabled(True)
            self.dial.setEnabled(True)
            self.checkboxL.setEnabled(True)
            self.checkboxM.setEnabled(True)
            self.checkboxX.setEnabled(True)
            self.checkboxJ.setEnabled(True)
            self.checkboxV.setEnabled(True)
            self.checkboxS.setEnabled(True)
            self.checkboxD.setEnabled(True)
            self.aceptar.setEnabled(True)
        else:
            self.hora_rego.setEnabled(False)
            self.text.setEnabled(False)
            self.diario.setEnabled(False)
            self.semanal.setEnabled(False)
            self.antixiada.setEnabled(False)
            self.chuvia.setEnabled(False)
            self.dial.setEnabled(False)
            self.checkboxL.setEnabled(False)
            self.checkboxM.setEnabled(False)
            self.checkboxX.setEnabled(False)
            self.checkboxJ.setEnabled(False)
            self.checkboxV.setEnabled(False)
            self.checkboxS.setEnabled(False)
            self.checkboxD.setEnabled(False)
            self.aceptar.setEnabled(False)

    # Recibe el número actual de la ruleta (estado) y actualiza la etiqueta de texto
    def textoRego(self, estado):
        self.duracion_rego.setText("Duracion Rego " + str(estado))

    # Valida que lo escrito en la caja de texto tenga formato HH:MM al pulsar Enter
    def comporbarHora(self):
        hora = self.text.text()  # Lee lo que escribió el usuario

        # Comprueba que tenga 5 caracteres (ej. "12:30") y que el tercero (índice 2) sea ":"
        if len(hora) != 5 or hora[2] != ":":
            # Añade el mensaje de error a la consola sin borrar lo que ya había escrito antes
            self.texto.setText(self.texto.toPlainText() + hora + "\nError, formato invalido\n")
        else:
            try:
                # Convierte las dos primeras letras a número (horas) y las dos últimas a número (minutos)
                horas = int(hora[0] + hora[1])
                minutos = int(hora[3] + hora[4])

                # Comprueba que sean horas y minutos reales (00-23 y 00-59)
                if horas > 23 or minutos > 59:
                    self.texto.setText(self.texto.toPlainText() + hora + "\nError, formato invalido\n")
                else:
                    self.texto.setText(self.texto.toPlainText() + hora + "\nCorrecto\n")

            # Si el usuario escribió letras en vez de números (ej. "ab:cd"), int() falla y entra aquí
            except ValueError:
                self.texto.setText(self.texto.toPlainText() + hora + "\nError, formato invalido\n")

    # Recoge todos los datos marcados en el formulario y los imprime en la pantalla Consola
    def activarAceptar(self):
        num_zona = "Zona 1"
        hora_comezo = self.text.text()          # Lee el texto de la hora
        duracion = self.duracion_rego.text()    # Lee el texto de la etiqueta de duración

        # Va sumando las iniciales de los días que estén marcados (.isChecked() == True)
        dias = ""
        if self.checkboxL.isChecked():
            dias += "L "
        if self.checkboxM.isChecked():
            dias += "M "
        if self.checkboxX.isChecked():
            dias += "X "
        if self.checkboxJ.isChecked():
            dias += "J "
        if self.checkboxV.isChecked():
            dias += "V "
        if self.checkboxS.isChecked():
            dias += "S "
        if self.checkboxD.isChecked():
            dias += "D "

        # Va sumando las opciones que estén marcadas
        opcions = ""
        if self.diario.isChecked():
            opcions += "Diario "
        if self.semanal.isChecked():
            opcions += "Semana "
        if self.antixiada.isChecked():
            opcions += "Antixiada "
        if self.chuvia.isChecked():
            opcions += "Chuvia "

        # Escribe todo el resumen en la consola (QTextEdit) conservando el texto anterior
        self.texto.setText(self.texto.toPlainText() + num_zona + "\n" + hora_comezo + "\n" + duracion + "\n" + dias + "\n" + opcions)


# 3. ARRANQUE DEL PROGRAMA (Siempre igual)
if __name__ == '__main__':
    app = QApplication(sys.argv)   # Crea la aplicación
    window = VentanaPrincipal()    # Crea nuestra ventana
    window.show()                  # La muestra en pantalla
    sys.exit(app.exec())           # Mantiene la ventana abierta esperando clics