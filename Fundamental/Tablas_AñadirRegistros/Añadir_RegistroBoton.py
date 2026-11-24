import sys
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QDialog,
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


# --- PANTALLA 2: VENTANA SECUNDARIA DEL FORMULARIO ---
class FiestraFormulario(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Novo Rexistro")
        self.resize(350, 200)

        caixaV = QVBoxLayout()
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

        caixaV.addLayout(formulario)

        # Botones Aceptar y Cancelar
        caixaBotons = QHBoxLayout()
        self.btnAceptar = QPushButton("Aceptar")
        self.btnCancelar = QPushButton("Cancelar")

        self.btnAceptar.clicked.connect(self.validar_e_aceptar)
        self.btnCancelar.clicked.connect(self.cancelar_e_limpar)

        caixaBotons.addWidget(self.btnAceptar)
        caixaBotons.addWidget(self.btnCancelar)

        caixaV.addLayout(caixaBotons)
        self.setLayout(caixaV)

    def validar_e_aceptar(self):
        if not self.txtNome.text().strip() or not self.txtDni.text().strip():
            QMessageBox.warning(self, "Campos baleiros", "Por favor, cubre o Nome e o DNI antes de aceptar.")
            return
        # Cierra la ventana devolviendo QDialog.DialogCode.Accepted
        self.accept()

    def cancelar_e_limpar(self):
        self.limpar_campos()
        # Cierra la ventana devolviendo QDialog.DialogCode.Rejected
        self.reject()

    def limpar_campos(self):
        self.txtNome.clear()
        self.txtDni.clear()
        self.cmbXenero.setCurrentIndex(0)
        self.chkFalecido.setChecked(False)

    def obter_datos(self):
        return [
            self.txtNome.text().strip(),
            self.txtDni.text().strip(),
            self.cmbXenero.currentText(),
            self.chkFalecido.isChecked(),
        ]


# --- PANTALLA 1: VENTANA PRINCIPAL CON LA TABLA ---
class FiestraPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exemplo QTableView")
        self.resize(500, 350)

        datos = [
            ["Nome", "Dni", "Xenero", "Falecido"],
            ["Ana Perez", "1111R", "Muller", False],
            ["Paco Porras", "2222T", "Home", True],
            ["Roque Vila", "3333H", "Home", False],
        ]

        self.modelo = ModeloTaboa(datos)

        caixaV = QVBoxLayout()

        self.tvwTaboa = QTableView()
        self.tvwTaboa.setModel(self.modelo)
        caixaV.addWidget(self.tvwTaboa)

        # Botón para abrir la segunda pantalla
        self.btnNovo = QPushButton("Engadir Rexistro")
        self.btnNovo.clicked.connect(self.abrir_formulario)
        caixaV.addWidget(self.btnNovo)

        contedor = QWidget()
        contedor.setLayout(caixaV)
        self.setCentralWidget(contedor)

        self.show()

    def abrir_formulario(self):
        dialogo = FiestraFormulario(self)
        # .exec() abre la segunda ventana y espera hasta que se cierre
        if dialogo.exec() == QDialog.DialogCode.Accepted:
            novos_datos = dialogo.obter_datos()
            self.modelo.engadir_fila(novos_datos)


if __name__ == "__main__":
    aplicacion = QApplication(sys.argv)
    fiestra = FiestraPrincipal()
    aplicacion.exec()