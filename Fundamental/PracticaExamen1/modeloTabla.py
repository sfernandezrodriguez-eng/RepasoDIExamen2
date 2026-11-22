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
        if indice.isValid():
            fila = indice.row() + 1
            col = indice.column()
            dato = self.tabla[fila][col]

            # TEXTO DE LAS CELDAS (Todas menos la columna 3, que es el checkbox)
            if rol == Qt.ItemDataRole.DisplayRole:
                if col != 3:
                    return str(dato)

            # CHECKBOX EN LA COLUMNA 3 ("Activada")
            if rol == Qt.ItemDataRole.CheckStateRole:
                if col == 3:
                    return Qt.CheckState.Checked if dato else Qt.CheckState.Unchecked

            # COLORES CONDICIONALES POR CELDA
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
                    if zona == "Zona 1":
                        return QColor("lightgreen")
                    elif zona == "Zona 2":
                        return QColor("lightyellow")

    def setData(self, indice, valor, rol):
        fila = indice.row() + 1
        col = indice.column()

        if rol == Qt.ItemDataRole.EditRole:
            # Editar Hora (columna 1) validando hh:mm
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

            # Editar Nombre del Granjero (columna 4) sin dejarlo vacío
            elif col == 4:
                if valor.strip() != "":
                    self.tabla[fila][4] = valor.strip().capitalize()
                    self.dataChanged.emit(indice, indice)
                    return True

            # Editar Género (columna 5) obligando a que sea Home o Muller
            elif col == 5:
                if valor.strip().lower() in ("home", "muller"):
                    self.tabla[fila][5] = valor.strip().capitalize()
                    # Emitimos cambio en col 4 y col 5 para que ambas cambien de color al instante
                    idx_nombre = self.index(indice.row(), 4)
                    self.dataChanged.emit(idx_nombre, indice)
                    return True

        # Marcar/Desmarcar Checkbox (columna 3)
        if rol == Qt.ItemDataRole.CheckStateRole:
            if col == 3:
                self.tabla[fila][3] = (valor == Qt.CheckState.Checked.value)
                self.dataChanged.emit(indice, indice)
                return True

        return False

    def headerData(self, seccion, orientacion, rol):
        if rol == Qt.ItemDataRole.DisplayRole:
            if orientacion == Qt.Orientation.Horizontal:
                return self.tabla[0][seccion]
        if rol == Qt.ItemDataRole.BackgroundRole:
            return QColor("lightgray")

    def flags(self, indice):
        condicions = Qt.ItemFlag.ItemIsEnabled
        col = indice.column()

        # Columnas editables con doble clic: Hora (1), Granjero (4) y Género (5)
        if col in (1, 4, 5):
            condicions = condicions | Qt.ItemFlag.ItemIsEditable

        # Columna checkbox: Activada (3)
        if col == 3:
            condicions = condicions | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEditable

        return condicions

    # Método para insertar nuevas filas desde el formulario
    def engadirFila(self, nova_fila):
        fila_nueva_idx = self.rowCount(QModelIndex())
        self.beginInsertRows(QModelIndex(), fila_nueva_idx, fila_nueva_idx)
        self.tabla.append(nova_fila)
        self.endInsertRows()