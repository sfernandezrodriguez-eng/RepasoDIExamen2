import sys
import math

# 1. IMPORTACIONES
# Qt es necesario para decirle al QSlider si es horizontal o vertical (Qt.Orientation.Horizontal)
from PyQt6.QtCore import Qt
# El asterisco (*) importa de golpe todos los widgets (QPushButton, QLabel, QSlider, etc.) sin escribirlos uno a uno
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QColor, QPalette


# 2. LA VENTANA PRINCIPAL
class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ExamenB")  # Título de la ventana

        self.setMinimumSize(100, 100)
        self.setMaximumSize(1000, 1000)

        # Organizador principal de toda la ventana (de arriba a abajo)
        maia = QVBoxLayout()

        # =========================================================================
        # PANTALLA 0: CONFIGURACIÓN (Formulario principal)
        # =========================================================================
        conf = QWidget()  # Caja vacía para esta pantalla
        pantalla_conf = QGridLayout()  # Organizador tipo tabla de Excel

        # --- Fila 0 ---
        self.activada = QLabel("Activada")
        pantalla_conf.addWidget(self.activada, 0, 0)  # Fila 0, Col 0

        self.checkbox = QCheckBox()  # Casilla de verificación
        pantalla_conf.addWidget(self.checkbox, 0, 1)  # Fila 0, Col 1

        # --- Fila 1 ---
        self.hora_rego = QLabel("Hora de comenzo do rego")
        pantalla_conf.addWidget(self.hora_rego, 1, 0)  # Fila 1, Col 0

        self.text = QLineEdit()  # Caja de texto de una línea
        pantalla_conf.addWidget(self.text, 1, 1)  # Fila 1, Col 1

        # --- Bloque derecho: Días en una mini-tabla de 2 columnas ---
        vertical = QVBoxLayout()  # Organizador vertical para el título "Dias" y la rejilla de checkboxes

        dias = QLabel("Dias")
        vertical.addWidget(dias)

        verticalGrid = QGridLayout()  # Mini-tabla dentro de la tabla grande para poner los días en 2 columnas

        self.checkboxL = QCheckBox("Lunes")
        self.checkboxM = QCheckBox("Martes")
        self.checkboxX = QCheckBox("Miercoles")
        self.checkboxJ = QCheckBox("Jueves")
        self.checkboxV = QCheckBox("Viernes")
        self.checkboxS = QCheckBox("Sabado")
        self.checkboxD = QCheckBox("Domingo")

        # Colocamos los días en 2 columnas (0 y 1) y 4 filas (0, 1, 2, 3)
        verticalGrid.addWidget(self.checkboxL, 0, 0)
        verticalGrid.addWidget(self.checkboxM, 0, 1)
        verticalGrid.addWidget(self.checkboxX, 1, 0)
        verticalGrid.addWidget(self.checkboxJ, 1, 1)
        verticalGrid.addWidget(self.checkboxV, 2, 0)
        verticalGrid.addWidget(self.checkboxS, 2, 1)
        verticalGrid.addWidget(self.checkboxD, 3, 0)

        vertical.addLayout(verticalGrid)  # Metemos la mini-tabla dentro del bloque vertical

        self.aceptar = QPushButton("Aceptar")
        vertical.addWidget(self.aceptar)

        # Metemos todo el bloque derecho en la Fila 2, Columna 3 de la tabla principal
        pantalla_conf.addLayout(vertical, 2, 3)

        # --- Fila 2 (Izquierda): Barra deslizante (QSlider) en vez de ruleta (QDial) ---
        self.duracion_rego = QLabel("Duracion Rego 0")
        pantalla_conf.addWidget(self.duracion_rego, 2, 0)  # Fila 2, Col 0

        # DIFERENCIA CON EXAMEN A: Aquí usa QSlider horizontal en lugar de QDial
        self.slide = QSlider(Qt.Orientation.Horizontal)
        self.slide.setRange(0, 600)  # Valores posibles de la barra: de 0 a 600
        pantalla_conf.addWidget(self.slide, 2, 1)  # Fila 2, Col 1

        # --- Fila 3 y 4: Opciones y Desplegable ---
        self.opcions = QLabel("Opcions")
        pantalla_conf.addWidget(self.opcions, 3, 0)  # Fila 3, Col 0

        horizontal = QHBoxLayout()  # Fila horizontal para el desplegable y los 2 checkboxes

        self.antixiada = QCheckBox("Antixiada")
        self.chuvia = QCheckBox("Chuvia")

        # DIFERENCIA CON EXAMEN A: Aquí "Semanal" y "Diario" van en un desplegable (QComboBox) en vez de RadioButtons
        self.dropMenu = QComboBox()
        self.dropMenu.addItems(["Semanal", "Diario"])  # Índice 0 = "Semanal", Índice 1 = "Diario"
        self.dropMenu.setCurrentIndex(0)  # Empieza seleccionando "Semanal"

        horizontal.addWidget(self.dropMenu)
        horizontal.addWidget(self.antixiada)
        horizontal.addWidget(self.chuvia)

        # Metemos la fila horizontal en Fila 4, Col 0, ocupando 1 fila y 3 columnas
        pantalla_conf.addLayout(horizontal, 4, 0, 1, 3)

        # Coloca el botón Aceptar en la Fila 5, Columna 2
        pantalla_conf.addWidget(self.aceptar, 5, 2)

        # Cerramos la pantalla 0
        conf.setLayout(pantalla_conf)

        # =========================================================================
        # PANTALLA 1: ZOA 2
        # =========================================================================
        zoa = QWidget()
        pantalla_zoa = QGridLayout()
        etiqueta = QLabel("Etiqueta")
        pantalla_zoa.addWidget(etiqueta, 0, 0)
        zoa.setLayout(pantalla_zoa)

        # =========================================================================
        # PANTALLA 2: CONSOLA
        # =========================================================================
        consola = QWidget()
        pantalla_consola = QGridLayout()
        self.texto = QTextEdit()  # Caja de texto multilínea para mostrar mensajes
        pantalla_consola.addWidget(self.texto, 0, 0)
        consola.setLayout(pantalla_consola)

        # =========================================================================
        # BOTONES INFERIORES DE NAVEGACIÓN (DIFERENCIA CLAVE CON EXAMEN A)
        # =========================================================================
        # En el Examen A se cambiaba de pantalla con un QComboBox arriba.
        # Aquí se cambia de pantalla con 3 QPushButton abajo.
        botones = QHBoxLayout()
        self.conf1 = QPushButton("Configuracion 1")
        self.conf2 = QPushButton("Configuracion 2")
        self.console = QPushButton("Consola")

        botones.addWidget(self.conf1)
        botones.addWidget(self.conf2)
        botones.addWidget(self.console)

        # Conectamos cada botón a su función para cambiar de tarjeta
        self.conf1.clicked.connect(self.mostrarConf1)
        self.conf2.clicked.connect(self.mostrarConf2)
        self.console.clicked.connect(self.mostrarConsola)

        # =========================================================================
        # BARAJA DE PANTALLAS (QStackedLayout) Y MONTAJE FINAL
        # =========================================================================
        self.tarxetas = QStackedLayout()
        self.tarxetas.addWidget(conf)     # Índice 0
        self.tarxetas.addWidget(zoa)      # Índice 1
        self.tarxetas.addWidget(consola)  # Índice 2

        # En 'maia' ponemos primero las pantallas arriba y luego la fila de botones abajo
        maia.addLayout(self.tarxetas)
        maia.addLayout(botones)

        # OBLIGATORIO en QMainWindow: meter 'maia' en un QWidget central
        contenedor = QWidget()
        contenedor.setLayout(maia)
        self.setCentralWidget(contenedor)

        # =========================================================================
        # CONEXIÓN DE EVENTOS (La lógica del programa)
        # =========================================================================
        # 1. Al cambiar el checkbox 'Activada', escribe en la consola
        self.checkbox.stateChanged.connect(self.printActivada)

        # 2. Al mover la barra deslizante, actualiza el texto de duración
        self.slide.valueChanged.connect(self.textoRego)

        # 3. Al cambiar el desplegable ("Semanal" / "Diario"), bloquea o desbloquea los días
        self.dropMenu.currentIndexChanged.connect(self.bloquear)

    # =============================================================================
    # FUNCIONES
    # =============================================================================

    # Escribe "Zoa activada" en la consola sin borrar lo que había antes
    def printActivada(self):
        self.texto.setText(self.texto.toPlainText() + "Zoa activada\n")

    # Recibe el número actual del QSlider (estado) y actualiza la etiqueta
    def textoRego(self, estado):
        self.duracion_rego.setText("Duracion Rego " + str(estado))

    # Bloquea los checkboxes de los días si se elige la opción 0 ("Semanal") y los activa si se elige "Diario"
    def bloquear(self, index):
        if index == 0:  # 0 es la primera opción del QComboBox ("Semanal")
            self.checkboxL.setEnabled(False)
            self.checkboxM.setEnabled(False)
            self.checkboxX.setEnabled(False)
            self.checkboxJ.setEnabled(False)
            self.checkboxV.setEnabled(False)
            self.checkboxS.setEnabled(False)
            self.checkboxD.setEnabled(False)
        else:           # Cualquier otra opción (1 = "Diario") los vuelve a activar
            self.checkboxL.setEnabled(True)
            self.checkboxM.setEnabled(True)
            self.checkboxX.setEnabled(True)
            self.checkboxJ.setEnabled(True)
            self.checkboxV.setEnabled(True)
            self.checkboxS.setEnabled(True)
            self.checkboxD.setEnabled(True)

    # Funciones de los 3 botones de abajo para cambiar la pantalla visible del QStackedLayout
    def mostrarConf1(self):
        self.tarxetas.setCurrentIndex(0)  # Muestra 'conf'

    def mostrarConf2(self):
        self.tarxetas.setCurrentIndex(1)  # Muestra 'zoa'

    def mostrarConsola(self):
        self.tarxetas.setCurrentIndex(2)  # Muestra 'consola'


# 3. ARRANQUE DEL PROGRAMA
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VentanaPrincipal()
    window.show()
    sys.exit(app.exec())