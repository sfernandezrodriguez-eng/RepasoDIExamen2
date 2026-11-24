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
    QGridLayout,
    QGroupBox,
    QWidget,
    QLineEdit,
    QComboBox,
    QCheckBox,
    QPushButton,
    QMessageBox,
    QLabel,
    QButtonGroup,
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
        # La fila 0 (cabecera) no debe ser seleccionable
        if index.row() == 0:
            return Qt.ItemFlag.ItemIsEnabled

        base_flags = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        if isinstance(self._datos[index.row()][index.column()], bool):
            return base_flags | Qt.ItemFlag.ItemIsUserCheckable
        return base_flags

    def setData(self, index, value, role):
        if (
            role == Qt.ItemDataRole.CheckStateRole
            and isinstance(self._datos[index.row()][index.column()], bool)
        ):
            self._datos[index.row()][index.column()] = value == Qt.CheckState.Checked.value
            self.dataChanged.emit(index, index)
            return True
        return False

    def engadir_fila(self, nova_fila):
        pos = len(self._datos)
        self.beginInsertRows(QModelIndex(), pos, pos)
        self._datos.append(nova_fila)
        self.endInsertRows()

    def modificar_fila(self, fila, novos_datos):
        if 0 < fila < len(self._datos):
            self._datos[fila] = novos_datos
            top_left = self.index(fila, 0)
            bottom_right = self.index(fila, self.columnCount() - 1)
            self.dataChanged.emit(top_left, bottom_right)

    def eliminar_fila(self, fila):
        if 0 < fila < len(self._datos):
            self.beginRemoveRows(QModelIndex(), fila, fila)
            del self._datos[fila]
            self.endRemoveRows()


class FiestraPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("V2: Xestión por Modos")
        self.resize(560, 480)

        self.modo_actual = None  # "novo", "modificar", "borrar" o None
        self.fila_seleccionada = None

        datos = [
            ["Nome", "Dni", "Xenero", "Falecido"],
            ["Ana Perez", "1111R", "Muller", False],
            ["Paco Porras", "2222T", "Home", True],
            ["Roque Vila", "3333H", "Home", False],
        ]

        self.modelo = ModeloTaboa(datos)
        caixaV = QVBoxLayout()

        # 1. Tabla superior
        self.tvwTaboa = QTableView()
        self.tvwTaboa.setModel(self.modelo)
        self.tvwTaboa.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tvwTaboa.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tvwTaboa.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tvwTaboa.clicked.connect(self.al_seleccionar_fila)
        caixaV.addWidget(self.tvwTaboa)

        # 2. Botones de selección de modo (según boceto)
        caixaModos = QHBoxLayout()
        self.btnModoNovo = QPushButton("Novo Usuario")
        self.btnModoModificar = QPushButton("Modificar")
        self.btnModoBorrar = QPushButton("Borrar")

        self.grupoBotonsModo = QButtonGroup(self)
        self.grupoBotonsModo.setExclusive(True)

        for btn in (self.btnModoNovo, self.btnModoModificar, self.btnModoBorrar):
            btn.setCheckable(True)
            self.grupoBotonsModo.addButton(btn)
            caixaModos.addWidget(btn)

        self.btnModoNovo.clicked.connect(lambda: self.cambiar_modo("novo"))
        self.btnModoModificar.clicked.connect(lambda: self.cambiar_modo("modificar"))
        self.btnModoBorrar.clicked.connect(lambda: self.cambiar_modo("borrar"))

        caixaV.addLayout(caixaModos)

        # 3. Etiqueta indicadora de modo (según boceto: "Modo: ...")
        self.lblModo = QLabel("Modo: Ningún modo seleccionado")
        self.lblModo.setStyleSheet("font-weight: bold; margin-top: 4px;")
        caixaV.addWidget(self.lblModo)

        # 4. Formulario inferior (disposición según boceto)
        self.grupoForm = QGroupBox()
        layoutForm = QVBoxLayout()
        grid = QGridLayout()

        self.txtNome = QLineEdit()
        self.txtDni = QLineEdit()
        self.cmbXenero = QComboBox()
        self.cmbXenero.addItems(["Muller", "Home"])
        self.chkFalecido = QCheckBox("Falecido")

        grid.addWidget(QLabel("Nome:"), 0, 0)
        grid.addWidget(self.txtNome, 0, 1, 1, 2)

        grid.addWidget(QLabel("DNI:"), 1, 0)
        grid.addWidget(self.txtDni, 1, 1, 1, 2)

        grid.addWidget(QLabel("Xénero:"), 2, 0)
        grid.addWidget(self.cmbXenero, 2, 1)
        grid.addWidget(self.chkFalecido, 2, 2)

        layoutForm.addLayout(grid)

        caixaBotons = QHBoxLayout()
        self.btnAceptar = QPushButton("Aceptar")
        self.btnCancelar = QPushButton("Cancelar")
        self.btnAceptar.clicked.connect(self.executar_accion)
        self.btnCancelar.clicked.connect(self.cancelar_accion)

        caixaBotons.addWidget(self.btnAceptar)
        caixaBotons.addWidget(self.btnCancelar)
        layoutForm.addLayout(caixaBotons)

        self.grupoForm.setLayout(layoutForm)
        caixaV.addWidget(self.grupoForm)

        contedor = QWidget()
        contedor.setLayout(caixaV)
        self.setCentralWidget(contedor)

        # Estado inicial bloqueado hasta elegir modo
        self.actualizar_estado_controles()
        self.show()

    def cambiar_modo(self, modo):
        self.modo_actual = modo
        self.fila_seleccionada = None
        self.tvwTaboa.clearSelection()
        self.limpar_formulario()

        textos_modo = {
            "novo": "Modo: Novo Usuario",
            "modificar": "Modo: Modificar (selecciona unha fila na táboa)",
            "borrar": "Modo: Borrar (selecciona unha fila na táboa)",
        }
        self.lblModo.setText(textos_modo[modo])
        self.actualizar_estado_controles()

        if modo == "novo":
            self.txtNome.setFocus()

    def actualizar_estado_controles(self):
        # Sin modo seleccionado: todo deshabilitado
        if self.modo_actual is None:
            self.set_campos_habilitados(False)
            self.btnAceptar.setEnabled(False)
            self.btnCancelar.setEnabled(False)
            return

        # Modo Novo: campos y botones activos
        if self.modo_actual == "novo":
            self.set_campos_habilitados(True)
            self.btnAceptar.setEnabled(True)
            self.btnCancelar.setEnabled(True)

        # Modo Modificar: activo solo cuando hay fila elegida
        elif self.modo_actual == "modificar":
            ten_fila = self.fila_seleccionada is not None
            self.set_campos_habilitados(ten_fila)
            self.btnAceptar.setEnabled(ten_fila)
            self.btnCancelar.setEnabled(ten_fila)

        # Modo Borrar: campos de solo lectura para visualizar, aceptar activo al elegir fila
        elif self.modo_actual == "borrar":
            ten_fila = self.fila_seleccionada is not None
            self.set_campos_habilitados(False)
            self.btnAceptar.setEnabled(ten_fila)
            self.btnCancelar.setEnabled(ten_fila)

    def set_campos_habilitados(self, estado):
        self.txtNome.setEnabled(estado)
        self.txtDni.setEnabled(estado)
        self.cmbXenero.setEnabled(estado)
        self.chkFalecido.setEnabled(estado)

    def al_seleccionar_fila(self, index):
        fila = index.row()
        if fila == 0:  # Ignorar cabecera
            return

        if self.modo_actual in ("modificar", "borrar"):
            self.fila_seleccionada = fila
            self.cargar_datos_fila(fila)
            self.actualizar_estado_controles()

    def cargar_datos_fila(self, fila):
        datos_fila = self.modelo._datos[fila]
        self.txtNome.setText(datos_fila[0])
        self.txtDni.setText(datos_fila[1])
        self.cmbXenero.setCurrentText(datos_fila[2])
        self.chkFalecido.setChecked(datos_fila[3])

    def executar_accion(self):
        if self.modo_actual == "novo":
            nome = self.txtNome.text().strip()
            dni = self.txtDni.text().strip()
            if not nome or not dni:
                QMessageBox.warning(self, "Aviso", "Cubre Nome e DNI.")
                return
            self.modelo.engadir_fila(
                [nome, dni, self.cmbXenero.currentText(), self.chkFalecido.isChecked()]
            )
            self.limpar_formulario()
            self.txtNome.setFocus()

        elif self.modo_actual == "modificar" and self.fila_seleccionada is not None:
            nome = self.txtNome.text().strip()
            dni = self.txtDni.text().strip()
            if not nome or not dni:
                QMessageBox.warning(self, "Aviso", "Cubre Nome e DNI.")
                return
            self.modelo.modificar_fila(
                self.fila_seleccionada,
                [nome, dni, self.cmbXenero.currentText(), self.chkFalecido.isChecked()],
            )
            self.limpar_seleccion_e_formulario()

        elif self.modo_actual == "borrar" and self.fila_seleccionada is not None:
            self.modelo.eliminar_fila(self.fila_seleccionada)
            self.limpar_seleccion_e_formulario()

    def cancelar_accion(self):
        # Si estaba modificando, al limpiar y deseleccionar no se guarda ningún cambio en el modelo
        if self.modo_actual == "novo":
            self.limpar_formulario()
            self.txtNome.setFocus()
        elif self.modo_actual in ("modificar", "borrar"):
            self.limpar_seleccion_e_formulario()

    def limpar_seleccion_e_formulario(self):
        self.fila_seleccionada = None
        self.tvwTaboa.clearSelection()
        self.limpar_formulario()
        self.actualizar_estado_controles()

    def limpar_formulario(self):
        self.txtNome.clear()
        self.txtDni.clear()
        self.cmbXenero.setCurrentIndex(0)
        self.chkFalecido.setChecked(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    fiestra = FiestraPrincipal()
    app.exec()



    """1. Si quieres añadir, quitar o cambiar campos (ej. añadir "Teléfono" o cambiar "Nome"):
    Los datos iniciales (FiestraPrincipal.__init__): Añade el nombre de la columna en la fila 0 de la lista datos y el valor por defecto en el resto de filas (ej. ["Nome", "Dni", "Xenero", "Falecido", "Teléfono"]).
    La interfaz (FiestraPrincipal.__init__): Crea el nuevo widget (ej. self.txtTelefono = QLineEdit()) y añádelo al grid indicando su fila y columna con grid.addWidget(...).
    El control de bloqueo (set_campos_habilitados): Añade self.txtTelefono.setEnabled(estado) para que el campo se active o desactive automáticamente según el modo.
    Carga y limpieza (cargar_datos_fila y limpar_formulario):
        En cargar_datos_fila: lee la nueva posición de la lista (self.txtTelefono.setText(datos_fila[4])).
        En limpar_formulario: vacía el campo (self.txtTelefono.clear()).   
    Guardado (executar_accion): Incluye el valor del nuevo campo dentro de las listas que se pasan a self.modelo.engadir_fila([...]) y self.modelo.modificar_fila(...)
    
    
2. Si quieres añadir un nuevo modo (ej. "Consultar" o "Duplicar"):
    El botón (FiestraPrincipal.__init__): Crea el nuevo QPushButton, añádelo al bucle for btn in (...) para que sea checkable y entre en self.grupoBotonsModo, y conecta su clic con lambda: self.cambiar_modo("nuevo_modo").
    El texto informativo (cambiar_modo): Añade la clave "nuevo_modo": "Modo: ..." en el diccionario textos_modo.
    El bloqueo de controles (actualizar_estado_controles): Añade un elif self.modo_actual == "nuevo_modo": indicando si los campos del formulario deben estar editables (True o False) y cuándo se activan Aceptar y Cancelar.
    La selección en la tabla (al_seleccionar_fila): Si el nuevo modo necesita cargar datos al pinchar una fila de la tabla, añádelo a la condición if self.modo_actual in ("modificar", "borrar", "nuevo_modo"):.
    La acción final (executar_accion y cancelar_accion): Añade un elif self.modo_actual == "nuevo_modo": en ambos métodos para programar qué debe ocurrir al pulsar Aceptar y qué debe limpiarse al pulsar Cancelar."""


    """Cambiar color en fila:
    
    if role == Qt.ItemDataRole.BackgroundRole and fila > 0:
    xenero = self._datos[fila][2]
    falecido = self._datos[fila][3]

    if falecido:  # Ejemplo: si está fallecido, toda la fila gris
        return QColor("#D3D3D3")
    elif xenero == "Muller":
        return QColor("#FFC0CB")
    elif xenero == "Home":
        return QColor("#ADD8E6")
        
        
        Cambiar color en algo especifico:
        # Ejemplo: pintar SOLO la celda del DNI (columna 1) en amarillo
if role == Qt.ItemDataRole.BackgroundRole and fila > 0 and columna == 1:
    return QColor("#FFFF99")

# Ejemplo: cambiar el color de la LETRA (ForegroundRole) solo si el DNI empieza por "1"
if role == Qt.ItemDataRole.ForegroundRole and fila > 0 and columna == 1:
    if str(valor).startswith("1"):
        return QColor("red")
        
        Cambiar color de la cabecera:
        if role == Qt.ItemDataRole.BackgroundRole and fila == 0:
    return QColor("#333333")  # Fondo oscuro para la cabecera

if role == Qt.ItemDataRole.ForegroundRole and fila == 0:
    return QColor("#FFFFFF")  # Texto blanco para la cabecera
        
    """