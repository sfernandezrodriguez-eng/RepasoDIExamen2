from PyQt6.QtCore import *
from PyQt6.QtGui import *


class ModeloTabla(QAbstractTableModel):
    def __init__(self, tabla):
        super().__init__()
        self.tabla = tabla

    def rowCount(self, indice):
        return len(self.tabla) - 1

    def columnCount(self, indice):
        return len(self.tabla[0])

    def data(self, indice, rol):
        if not indice.isValid():
            return None

        fila = indice.row() + 1
        col = indice.column()
        dato = self.tabla[fila][col]

        # 1. TEXTO DE LAS CELDAS (Todas menos la columna 3, que es el checkbox)
        if rol == Qt.ItemDataRole.DisplayRole:
            if col != 3:
                return str(dato)

        # 2. CHECKBOX EN LA COLUMNA 3 ("Activada")
        if rol == Qt.ItemDataRole.CheckStateRole:
            if col == 3:
                return Qt.CheckState.Checked if dato else Qt.CheckState.Unchecked

        # 3. ALINEACIÓN (Duración en columna 2 a la derecha)
        if rol == Qt.ItemDataRole.TextAlignmentRole:
            if col == 2:
                return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter

        # 4. FUENTE / NEGRITA (Si duración > 100 min)
        if rol == Qt.ItemDataRole.FontRole:
            if col == 2:
                minutos = int(str(dato).replace(" min", ""))
                if minutos > 100:
                    fuente = QFont()
                    fuente.setBold(True)
                    return fuente

        # 5. COLORES CONDICIONALES POR CELDA
        if rol == Qt.ItemDataRole.BackgroundRole:
            # Columnas 4 (Granjero) y 5 (Género): Azul si Muller, Rosa si Home
            if col in (4, 5):
                genero = self.tabla[fila][5]
                if genero == "Home":
                    return QColor("pink")
                elif genero == "Muller":
                    return QColor("lightblue")
            # Resto de columnas (0 a 3): color según la Zona
            else:
                zona = self.tabla[fila][0]
                if zona == "Zoa 1":
                    return QColor("lightgreen")
                elif zona == "Zoa 2":
                    return QColor("lightyellow")

    def setData(self, indice, valor, rol):
        fila = indice.row() + 1
        col = indice.column()

        if rol == Qt.ItemDataRole.EditRole:
            # Editar Hora (col 1) validando hh:mm
            if col == 1:
                if len(valor) == 5 and valor[2] == ":":
                    try:
                        h, m = int(valor[:2]), int(valor[3:])
                        if 0 <= h <= 23 and 0 <= m <= 59:
                            self.tabla[fila][1] = valor
                            self.dataChanged.emit(indice, indice)
                            return True
                    except ValueError:
                        pass

            # Editar Nombre del Granjero (col 4) sin dejarlo vacío
            elif col == 4:
                if valor.strip() != "":
                    self.tabla[fila][4] = valor.strip().capitalize()
                    self.dataChanged.emit(indice, indice)
                    return True

            # Editar Género (col 5) obligando a Home o Muller y repintando col 4 y 5
            elif col == 5:
                if valor.strip().lower() in ("home", "muller"):
                    self.tabla[fila][5] = valor.strip().capitalize()
                    idx_nombre = self.index(indice.row(), 4)
                    self.dataChanged.emit(idx_nombre, indice)
                    return True

        # Marcar/Desmarcar Checkbox (col 3)
        if rol == Qt.ItemDataRole.CheckStateRole:
            if col == 3:
                self.tabla[fila][3] = (valor == Qt.CheckState.Checked.value)
                # Emitimos cambio en toda la fila porque al activar/desactivar cambian los permisos de edición (flags)
                self.dataChanged.emit(self.index(indice.row(), 0), self.index(indice.row(), self.columnCount(None) - 1))
                return True

        return False

    def headerData(self, seccion, orientacion, rol):
        if rol == Qt.ItemDataRole.DisplayRole:
            if orientacion == Qt.Orientation.Horizontal:
                return self.tabla[0][seccion]
        if rol == Qt.ItemDataRole.BackgroundRole:
            return QColor("lightgray")

    def flags(self, indice):
        fila = indice.row() + 1
        col = indice.column()
        condicions = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

        # TRAMPA: Si la zona está activada (True), no se pueden editar los datos de esa fila
        esta_activada = self.tabla[fila][3]

        if col == 3:
            # El checkbox siempre se puede tocar para poder desactivarlo
            condicions = condicions | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEditable
        elif not esta_activada:
            if col in (1, 4, 5):
                condicions = condicions | Qt.ItemFlag.ItemIsEditable

        return condicions

    # Métodos propios para insertar y borrar filas
    def engadirFila(self, nova_fila):
        fila_idx = self.rowCount(QModelIndex())
        self.beginInsertRows(QModelIndex(), fila_idx, fila_idx)
        self.tabla.append(nova_fila)
        self.endInsertRows()

    def eliminarFila(self, fila_vista):
        if 0 <= fila_vista < self.rowCount(QModelIndex()):
            self.beginRemoveRows(QModelIndex(), fila_vista, fila_vista)
            self.tabla.pop(fila_vista + 1)
            self.endRemoveRows()