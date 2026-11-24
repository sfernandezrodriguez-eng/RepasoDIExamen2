import sys
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableView,
    QHeaderView,
    QAbstractItemView,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QGroupBox,
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
        fila, columna = index.row(), index.column()
        valor = self._datos[fila][columna]

        if role == Qt.ItemDataRole.BackgroundRole and fila > 0:
            xenero = self._datos[fila][2]
            if xenero == "Muller":
                return QColor("#FFC0CB")
            elif xenero == "Home":
                return QColor("#ADD8E6")

        if isinstance(valor, bool):
            if role == Qt.ItemDataRole.CheckStateRole:
                return Qt.CheckState.Checked if valor else Qt.CheckState.Unchecked
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            return valor

        return None

    def flags(self, index):
        if isinstance(self._datos[index.row()][index.column()], bool):
            return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable
        return Qt.ItemFlag.ItemIsEnabled

    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.CheckStateRole and isinstance(self._datos[index.row()][index.column()], bool):
            self._datos[index.row()][index.column()] = (value == Qt.CheckState.Checked.value)
            self.dataChanged.emit(index, index)
            return True
        return False

    def engadir_fila(self, nova_fila):
        pos = len(self._datos)
        self.beginInsertRows(QModelIndex(), pos, pos)
        self._datos.append(nova_fila)
        self.endInsertRows()

    def eliminar_por_dni(self, dni):
        for fila in range(1, len(self._datos)):
            if self._datos[fila][1].lower() == dni.lower():
                self.beginRemoveRows(QModelIndex(), fila, fila)
                del self._datos[fila]
                self.endRemoveRows()
                return True
        return False


class FiestraPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("V1: Xestión en Pantalla Única")
        self.resize(540, 460)

        datos = [
            ["Nome", "Dni", "Xenero", "Falecido"],
            ["Ana Perez", "1111R", "Muller", False],
            ["Paco Porras", "2222T", "Home", True],
            ["Roque Vila", "3333H", "Home", False],
        ]

        self.modelo = ModeloTaboa(datos)
        caixaV = QVBoxLayout()

        # Tabla ajustada al ancho
        self.tvwTaboa = QTableView()
        self.tvwTaboa.setModel(self.modelo)
        self.tvwTaboa.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.tvwTaboa.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        caixaV.addWidget(self.tvwTaboa)

        # Grupo Eliminar
        grupoEliminar = QGroupBox("Eliminar Rexistro")
        caixaEliminar = QHBoxLayout()
        self.txtEliminarDni = QLineEdit()
        self.txtEliminarDni.setPlaceholderText("Escribe o DNI a eliminar...")
        self.txtEliminarDni.returnPressed.connect(self.eliminar_rexistro)

        self.btnEliminar = QPushButton("Eliminar")
        self.btnEliminar.clicked.connect(self.eliminar_rexistro)

        caixaEliminar.addWidget(self.txtEliminarDni)
        caixaEliminar.addWidget(self.btnEliminar)
        grupoEliminar.setLayout(caixaEliminar)
        caixaV.addWidget(grupoEliminar)

        # Grupo Formulario
        grupoForm = QGroupBox("Novo Rexistro")
        layoutForm = QVBoxLayout()
        formulario = QFormLayout()

        self.txtNome = QLineEdit()
        self.txtDni = QLineEdit()
        self.cmbXenero = QComboBox()
        self.cmbXenero.addItems(["Muller", "Home"])
        self.chkFalecido = QCheckBox()

        formulario.addRow("Nome:", self.txtNome)
        formulario.addRow("DNI:", self.txtDni)
        formulario.addRow("Xénero:", self.cmbXenero)
        formulario.addRow("Falecido:", self.chkFalecido)
        layoutForm.addLayout(formulario)

        caixaBotons = QHBoxLayout()
        self.btnAceptar = QPushButton("Aceptar")
        self.btnCancelar = QPushButton("Cancelar")
        self.btnAceptar.clicked.connect(self.gardar_datos)
        self.btnCancelar.clicked.connect(self.limpar_formulario)

        caixaBotons.addWidget(self.btnAceptar)
        caixaBotons.addWidget(self.btnCancelar)
        layoutForm.addLayout(caixaBotons)
        grupoForm.setLayout(layoutForm)
        caixaV.addWidget(grupoForm)

        contedor = QWidget()
        contedor.setLayout(caixaV)
        self.setCentralWidget(contedor)
        self.show()

    def gardar_datos(self):
        nome = self.txtNome.text().strip()
        dni = self.txtDni.text().strip()
        if not nome or not dni:
            QMessageBox.warning(self, "Aviso", "Cubre Nome e DNI.")
            return
        self.modelo.engadir_fila([nome, dni, self.cmbXenero.currentText(), self.chkFalecido.isChecked()])
        self.limpar_formulario()

    def limpar_formulario(self):
        self.txtNome.clear()
        self.txtDni.clear()
        self.cmbXenero.setCurrentIndex(0)
        self.chkFalecido.setChecked(False)
        self.txtNome.setFocus()

    def eliminar_rexistro(self):
        dni = self.txtEliminarDni.text().strip()
        if not dni:
            return
        if self.modelo.eliminar_por_dni(dni):
            self.txtEliminarDni.clear()
        else:
            QMessageBox.warning(self, "Erro", "DNI non atopado.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    fiestra = FiestraPrincipal()
    app.exec()