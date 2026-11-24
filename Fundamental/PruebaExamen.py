import sys
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex, QTime, QRect
from PyQt6.QtGui import QColor, QPainter, QBrush, QPen, QFont
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
    QDial,
    QProgressBar,
    QLabel,
)


# 1. WIDGET CUSTOM: QDial con círculo central dinámico
class DialCaudal(QDial):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRange(0, 100)
        self.setNotchesVisible(True)
        self.setFixedSize(130, 130)

    def paintEvent(self, event):
        # Primero dejamos que Qt pinte la rueda y las marcas normales
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        valor = self.value()
        if valor < 50:
            cor = QColor("#28A745")  # Verde
        elif valor <= 80:
            cor = QColor("#FD7E14")  # Naranja
        else:
            cor = QColor("#DC3545")  # Rojo

        # Calculamos el rectángulo central
        centro = self.rect().center()
        radio = 26
        rect_circulo = QRect(centro.x() - radio, centro.y() - radio, radio * 2, radio * 2)

        painter.setBrush(QBrush(cor))
        painter.setPen(QPen(Qt.GlobalColor.darkGray, 2))
        painter.drawEllipse(rect_circulo)

        # Texto blanco centrado
        painter.setPen(QPen(Qt.GlobalColor.white))
        fonte = QFont()
        fonte.setBold(True)
        fonte.setPointSize(11)
        painter.setFont(fonte)
        painter.drawText(rect_circulo, Qt.AlignmentFlag.AlignCenter, str(valor))
        painter.end()


# 2. MODELO DE TABLA COMPLETO
class ModeloTaboa(QAbstractTableModel):
    def __init__(self, datos, cabeceiras):
        super().__init__()
        self._cabeceiras = cabeceiras
        self._datos_orixinais = datos      # Copia maestra (nunca se pierde al filtrar)
        self._datos = list(datos)          # Vista actual filtrada
        self._filtro_actual = ""

    def rowCount(self, index=QModelIndex()):
        return len(self._datos)

    def columnCount(self, index=QModelIndex()):
        return len(self._cabeceiras)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self._cabeceiras[section]
        return super().headerData(section, orientation, role)

    def data(self, index, role):
        if not index.isValid():
            return None

        fila, columna = index.row(), index.column()
        rexistro = self._datos[fila]
        valor = rexistro[columna]
        caudal = int(rexistro[3])
        emerxencia = rexistro[4]

        # Colores de fondo de toda la fila
        if role == Qt.ItemDataRole.BackgroundRole:
            if emerxencia:
                return QColor("#FFCCCC")
            elif caudal < 30:
                return QColor("#CCE5FF")

        # Negrita si está en emergencia
        if role == Qt.ItemDataRole.FontRole and emerxencia:
            fonte = QFont()
            fonte.setBold(True)
            return fonte

        # Alineación derecha para Caudal (%)
        if role == Qt.ItemDataRole.TextAlignmentRole and columna == 3:
            return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter

        # Checkbox nativo en columna Emergencia
        if columna == 4:
            if role == Qt.ItemDataRole.CheckStateRole:
                return Qt.CheckState.Checked if valor else Qt.CheckState.Unchecked
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            return str(valor)

        return None

    def flags(self, index):
        # Necesario ItemIsSelectable para poder seleccionar la fila y borrarla con Supr
        base = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        if index.column() == 4:
            return base | Qt.ItemFlag.ItemIsUserCheckable
        return base

    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.CheckStateRole and index.column() == 4:
            self._datos[index.row()][4] = (value == Qt.CheckState.Checked.value)
            # Emitimos el cambio en TODA la fila (col 0 a 4) para que cambie de color al instante
            inicio = self.index(index.row(), 0)
            fin = self.index(index.row(), self.columnCount() - 1)
            self.dataChanged.emit(inicio, fin)
            return True
        return False

    def engadir_fila(self, nova_fila):
        self._datos_orixinais.append(nova_fila)
        self.aplicar_filtro(self._filtro_actual)

    def eliminar_fila(self, fila_visible):
        if 0 <= fila_visible < len(self._datos):
            rexistro = self._datos[fila_visible]
            self._datos_orixinais.remove(rexistro)
            self.aplicar_filtro(self._filtro_actual)

    def aplicar_filtro(self, texto):
        self._filtro_actual = texto.strip().lower()
        self.beginResetModel()
        if not self._filtro_actual:
            self._datos = list(self._datos_orixinais)
        else:
            self._datos = [
                f for f in self._datos_orixinais
                if self._filtro_actual in f[0].lower() or self._filtro_actual in f[1].lower()
            ]
        self.endResetModel()

    def obter_estatisticas(self):
        total = len(self._datos_orixinais)
        if total == 0:
            return 0, 0.0, 0
        media = sum(int(f[3]) for f in self._datos_orixinais) / total
        alertas = sum(1 for f in self._datos_orixinais if f[4])
        return total, media, alertas


# 3. VENTANA PRINCIPAL
class FiestraPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Panel de Control de Reactor Térmico")
        self.resize(860, 480)

        cabeceiras = ["Turno", "Sector", "Hora Inicio", "Caudal (%)", "Emergencia"]
        datos = [
            ["TUR001", "Núcleo", "14:30", 85, True],
            ["TUR002", "Sur", "10:00", 25, False],
            ["TUR003", "Norte", "08:00", 40, False],
        ]

        self.modelo = ModeloTaboa(datos, cabeceiras)

        # Layout raíz vertical (arriba los 2 paneles, abajo la barra de totales)
        layoutPrincipal = QVBoxLayout()
        caixaSuperior = QHBoxLayout()

        # --- PANEL IZQUIERDO: Panel de Control ---
        grupoForm = QGroupBox("Panel de Control")
        layoutForm = QVBoxLayout()
        formulario = QFormLayout()

        self.txtTurno = QLineEdit()
        self.cmbSector = QComboBox()
        self.cmbSector.addItems(["Norte", "Sur", "Núcleo"])

        self.txtHora = QLineEdit()
        self.txtHora.setPlaceholderText("HH:MM (ej. 14:30)")

        self.dialCaudal = DialCaudal()
        self.progressCaudal = QProgressBar()
        self.progressCaudal.setRange(0, 100)
        self.progressCaudal.setTextVisible(True)

        self.chkEmerxencia = QCheckBox("Modo Emergencia")

        formulario.addRow("Identificador de turno:", self.txtTurno)
        formulario.addRow("Sector:", self.cmbSector)
        formulario.addRow("Hora Inicio:", self.txtHora)
        formulario.addRow("Caudal (%):", self.dialCaudal)
        formulario.addRow("Carga Térmica:", self.progressCaudal)
        formulario.addRow("", self.chkEmerxencia)
        layoutForm.addLayout(formulario)

        self.btnAceptar = QPushButton("Añadir Turno")
        layoutForm.addWidget(self.btnAceptar)
        grupoForm.setLayout(layoutForm)
        caixaSuperior.addWidget(grupoForm, 1)

        # --- PANEL DERECHO: Registro de Turnos (Buscador + Tabla dentro del GroupBox) ---
        grupoTaboa = QGroupBox("Registro de Turnos")
        layoutTaboa = QVBoxLayout()

        self.txtBuscar = QLineEdit()
        self.txtBuscar.setPlaceholderText("Buscar por turno o sector...")
        layoutTaboa.addWidget(self.txtBuscar)

        self.tvwTaboa = QTableView()
        self.tvwTaboa.setModel(self.modelo)
        self.tvwTaboa.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tvwTaboa.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tvwTaboa.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layoutTaboa.addWidget(self.tvwTaboa)

        grupoTaboa.setLayout(layoutTaboa)
        caixaSuperior.addWidget(grupoTaboa, 2)

        layoutPrincipal.addLayout(caixaSuperior)

        # --- BARRA INFERIOR DE RESUMEN ---
        self.lblResumo = QLabel()
        self.lblResumo.setStyleSheet("font-weight: bold; padding: 4px;")
        layoutPrincipal.addWidget(self.lblResumo)

        contedor = QWidget()
        contedor.setLayout(layoutPrincipal)
        self.setCentralWidget(contedor)

        # --- CONEXIÓN DE SEÑALES ---
        self.dialCaudal.valueChanged.connect(self.sincronizar_caudal)
        self.chkEmerxencia.toggled.connect(self.alternar_emerxencia)
        self.btnAceptar.clicked.connect(self.gardar_datos)
        self.txtBuscar.textChanged.connect(self.modelo.aplicar_filtro)

        # Recalcular totales cuando cambia cualquier dato del modelo
        self.modelo.dataChanged.connect(self.actualizar_resumo)
        self.modelo.rowsInserted.connect(self.actualizar_resumo)
        self.modelo.modelReset.connect(self.actualizar_resumo)

        # Estado inicial
        self.sincronizar_caudal(self.dialCaudal.value())
        self.actualizar_resumo()
        self.show()

    def sincronizar_caudal(self, valor):
        self.progressCaudal.setValue(valor)
        # Emboscada de la hoja oficial: invertir barra si supera 80
        self.progressCaudal.setInvertedAppearance(valor > 80)

    def alternar_emerxencia(self, activo):
        if activo:
            self.dialCaudal.setValue(100)
            self.dialCaudal.setEnabled(False)
            self.cmbSector.setCurrentText("Núcleo")
            self.cmbSector.setEnabled(False)
            self.btnAceptar.setText("REGISTRAR EMERGENCIA")
        else:
            self.dialCaudal.setEnabled(True)
            self.cmbSector.setEnabled(True)
            self.btnAceptar.setText("Añadir Turno")

    def gardar_datos(self):
        turno = self.txtTurno.text().strip()
        hora_txt = self.txtHora.text().strip()

        if not turno:
            QMessageBox.warning(self, "Aviso", "El identificador de turno es obligatorio.")
            return

        # Validación estricta HH:MM con QTime
        hora_valida = QTime.fromString(hora_txt, "HH:mm")
        if not hora_valida.isValid():
            QMessageBox.warning(self, "Hora inválida", "Introduce una hora válida en formato HH:MM (00:00 a 23:59).")
            return

        nova_fila = [
            turno,
            self.cmbSector.currentText(),
            hora_txt,
            self.dialCaudal.value(),
            self.chkEmerxencia.isChecked(),
        ]
        self.modelo.engadir_fila(nova_fila)
        self.limpar_formulario()

    def limpar_formulario(self):
        self.txtTurno.clear()
        self.txtHora.clear()
        self.chkEmerxencia.setChecked(False)
        self.dialCaudal.setValue(0)
        self.cmbSector.setCurrentIndex(0)
        self.txtTurno.setFocus()

    def actualizar_resumo(self):
        total, media, alertas = self.modelo.obter_estatisticas()
        self.lblResumo.setText(
            f"Total Turnos: {total} | Caudal Medio: {media:.1f}% | Alertas Activas: {alertas}"
        )

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete and self.tvwTaboa.hasFocus():
            indices = self.tvwTaboa.selectionModel().selectedRows()
            if indices:
                self.modelo.eliminar_fila(indices[0].row())
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    fiestra = FiestraPrincipal()
    sys.exit(app.exec())