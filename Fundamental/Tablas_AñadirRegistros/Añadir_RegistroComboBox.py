import sys
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableView,
    QStackedWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QWidget,
    QLineEdit,
    QComboBox,
    QCheckBox,
    QPushButton,
    QMessageBox,
    QLabel,
)


class ModeloTaboa(QAbstractTableModel):
    def __init__(self, datos):
        super().__init__()
        self._datos = datos

    def rowCount(self, index=QModelIndex()):
        return len(self._datos)

    def columnCount(self, index=QModelIndex()):
        return len(self._datos[0])

    def data(self, index, role):
        fila = index.row()
        columna = index.column()
        valor = self._datos[fila][columna]

        # 1. Color de fondo según el género
        if role == Qt.ItemDataRole.BackgroundRole:
            if fila > 0:
                xenero = self._datos[fila][2]
                if xenero == "Muller":
                    return QColor("#FFC0CB")  # Rosa claro
                elif xenero == "Home":
                    return QColor("#ADD8E6")  # Azul claro

        # 2. Checkbox para valores booleanos
        if isinstance(valor, bool):
            if role == Qt.ItemDataRole.CheckStateRole:
                return Qt.CheckState.Checked if valor else Qt.CheckState.Unchecked
            return None

        # 3. Texto normal
        if role == Qt.ItemDataRole.DisplayRole:
            return valor

        return None

    def flags(self, index):
        valor = self._datos[index.row()][index.column()]
        if isinstance(valor, bool):
            return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsSelectable
        return super().flags(index)

    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.CheckStateRole and isinstance(self._datos[index.row()][index.column()], bool):
            self._datos[index.row()][index.column()] = (value == Qt.CheckState.Checked.value)
            self.dataChanged.emit(index, index)
            return True
        return False

    def engadir_fila(self, nova_fila):
        posicion = len(self._datos)
        self.beginInsertRows(QModelIndex(), posicion, posicion)
        self._datos.append(nova_fila)
        self.endInsertRows()


class FiestraPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Xestión de Persoas - Selector de Pantallas")
        self.resize(500, 350)

        datos = [
            ["Nome", "Dni", "Xenero", "Falecido"],
            ["Ana Perez", "1111R", "Muller", False],
            ["Paco Porras", "2222T", "Home", True],
            ["Roque Vila", "3333H", "Home", False],
        ]

        self.modelo = ModeloTaboa(datos)

        # Layout general
        caixaPrincipal = QVBoxLayout()

        # --- BARRA SUPERIOR CON EL DESPLEGABLE ---
        barraSelector = QHBoxLayout()
        barraSelector.addWidget(QLabel("Seleccionar pantalla:"))

        self.cmbPantallas = QComboBox()
        self.cmbPantallas.addItems(["1. Táboa de Rexistros", "2. Novo Rexistro (Formulario)"])
        barraSelector.addWidget(self.cmbPantallas)

        caixaPrincipal.addLayout(barraSelector)

        # --- CONTENEDOR DE PANTALLAS (QStackedWidget) ---
        self.paxinas = QStackedWidget()

        # PANTALLA 0: Vista de la Tabla
        pantallaTaboa = QWidget()
        layoutTaboa = QVBoxLayout()
        self.tvwTaboa = QTableView()
        self.tvwTaboa.setModel(self.modelo)
        layoutTaboa.addWidget(self.tvwTaboa)
        pantallaTaboa.setLayout(layoutTaboa)

        # PANTALLA 1: Vista del Formulario
        pantallaFormulario = QWidget()
        layoutFormPrincipal = QVBoxLayout()
        formulario = QFormLayout()

        self.txtNome = QLineEdit()
        self.txtNome.setPlaceholderText("Ex: María López")

        self.txtDni = QLineEdit()
        self.txtDni.setPlaceholderText("Ex: 4444X")

        self.cmbXenero = QComboBox()
        self.cmbXenero.addItems(["Muller", "Home"])

        self.chkFalecido = QCheckBox()

        formulario.addRow("Nome:", self.txtNome)
        formulario.addRow("DNI:", self.txtDni)
        formulario.addRow("Xénero:", self.cmbXenero)
        formulario.addRow("Falecido:", self.chkFalecido)

        layoutFormPrincipal.addLayout(formulario)

        # Botones del formulario
        caixaBotons = QHBoxLayout()
        self.btnAceptar = QPushButton("Aceptar")
        self.btnCancelar = QPushButton("Cancelar")

        self.btnAceptar.clicked.connect(self.gardar_datos)
        self.btnCancelar.clicked.connect(self.limpar_formulario)

        caixaBotons.addWidget(self.btnAceptar)
        caixaBotons.addWidget(self.btnCancelar)
        layoutFormPrincipal.addLayout(caixaBotons)
        layoutFormPrincipal.addStretch()  # Empuja los campos hacia arriba

        pantallaFormulario.setLayout(layoutFormPrincipal)

        # Añadimos ambas pantallas al QStackedWidget (índice 0 y índice 1)
        self.paxinas.addWidget(pantallaTaboa)
        self.paxinas.addWidget(pantallaFormulario)

        # Conectamos el índice del desplegable directamente con el índice de QStackedWidget
        self.cmbPantallas.currentIndexChanged.connect(self.paxinas.setCurrentIndex)

        caixaPrincipal.addWidget(self.paxinas)

        contedor = QWidget()
        contedor.setLayout(caixaPrincipal)
        self.setCentralWidget(contedor)

        self.show()

    def gardar_datos(self):
        nome = self.txtNome.text().strip()
        dni = self.txtDni.text().strip()
        xenero = self.cmbXenero.currentText()
        falecido = self.chkFalecido.isChecked()

        if not nome or not dni:
            QMessageBox.warning(self, "Campos baleiros", "Por favor, cubre o Nome e o DNI antes de aceptar.")
            return

        self.modelo.engadir_fila([nome, dni, xenero, falecido])
        self.limpar_formulario()

        # Cambiamos automáticamente el desplegable a la pantalla de la tabla (índice 0)
        self.cmbPantallas.setCurrentIndex(0)

    def limpar_formulario(self):
        self.txtNome.clear()
        self.txtDni.clear()
        self.cmbXenero.setCurrentIndex(0)
        self.chkFalecido.setChecked(False)
        self.txtNome.setFocus()


if __name__ == "__main__":
    aplicacion = QApplication(sys.argv)
    fiestra = FiestraPrincipal()
    aplicacion.exec()