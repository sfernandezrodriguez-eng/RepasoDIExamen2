import sys
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableView,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QWidget,
    QLineEdit,
    QComboBox,
    QCheckBox,
    QPushButton,
    QMessageBox,
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
                    return QColor("light pink")  # Rosa claro
                elif xenero == "Home":
                    return QColor("light blue")  # Azul claro

        # 2. Checkbox para valores booleanos
        if isinstance(valor, bool):
            if role == Qt.ItemDataRole.CheckStateRole:
                return  Qt.CheckState.Checked if valor else Qt.CheckState.Unchecked

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

    # Método para añadir nuevas filas dinámicamente
    def engadir_fila(self, nova_fila):
        posicion = len(self._datos)
        # Avisamos a la vista que se va a insertar una fila en 'posicion'
        self.beginInsertRows(QModelIndex(), posicion, posicion)
        self._datos.append(nova_fila)
        # Confirmamos que la inserción ha terminado para que se repinte la tabla
        self.endInsertRows()


class FiestraPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exemplo QTableView con Formulario")
        self.resize(500, 450)

        datos = [
            ["Nome", "Dni", "Xenero", "Falecido"],
            ["Ana Perez", "1111R", "Muller", False],
            ["Paco Porras", "2222T", "Home", True],
            ["Roque Vila", "3333H", "Home", False],
        ]

        self.modelo = ModeloTaboa(datos)

        # Layout principal vertical
        caixaV = QVBoxLayout()

        # Tabla
        self.tvwTaboa = QTableView()
        self.tvwTaboa.setModel(self.modelo)
        caixaV.addWidget(self.tvwTaboa)

        # --- FORMULARIO ---
        formulario = QFormLayout()

        self.txtNome = QLineEdit()
        self.txtNome.setPlaceholderText("Ex: María López")

        self.txtDni = QLineEdit()
        self.txtDni.setPlaceholderText("Ex: 4444X")

        self.cmbXenero = QComboBox()
        self.cmbXenero.addItems(["Muller", "Home", "Outro"])

        self.chkFalecido = QCheckBox()

        formulario.addRow("Nome:", self.txtNome)
        formulario.addRow("DNI:", self.txtDni)
        formulario.addRow("Xénero:", self.cmbXenero)
        formulario.addRow("Falecido:", self.chkFalecido)

        caixaV.addLayout(formulario)

        # --- BOTÓNS ---
        caixaBotons = QHBoxLayout()

        self.btnAceptar = QPushButton("Aceptar")
        self.btnCancelar = QPushButton("Cancelar")

        # Conectamos los clics de los botones con sus funciones
        self.btnAceptar.clicked.connect(self.gardar_datos)
        self.btnCancelar.clicked.connect(self.limpar_formulario)

        caixaBotons.addWidget(self.btnAceptar)
        caixaBotons.addWidget(self.btnCancelar)

        caixaV.addLayout(caixaBotons)

        # Contenedor central
        contedor = QWidget()
        contedor.setLayout(caixaV)
        self.setCentralWidget(contedor)

        self.show()

    def gardar_datos(self):
        nome = self.txtNome.text().strip()
        dni = self.txtDni.text().strip()
        xenero = self.cmbXenero.currentText()
        falecido = self.chkFalecido.isChecked()

        # Validación básica para evitar filas vacías
        if not nome or not dni:
            QMessageBox.warning(self, "Campos baleiros", "Por favor, cubre o Nome e o DNI antes de aceptar.")
            return

        # Añadimos la fila al modelo y limpiamos el formulario
        self.modelo.engadir_fila([nome, dni, xenero, falecido])
        self.limpar_formulario()

    def limpar_formulario(self):
        self.txtNome.clear()
        self.txtDni.clear()
        self.cmbXenero.setCurrentIndex(2)  # Vuelve a "Muller"
        self.chkFalecido.setChecked(False)
        self.txtNome.setFocus()  # Devuelve el cursor al campo Nome


if __name__ == "__main__":
    aplicacion = QApplication(sys.argv)
    fiestra = FiestraPrincipal()
    aplicacion.exec()