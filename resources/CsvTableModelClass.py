from PySide2 import QtCore
import csv


class CsvTableModel(QtCore.QAbstractTableModel):

    def __init__(self, tabella):
        super().__init__()
        #self.filename = csv_file
        self._headers = ["Riferimento",
                        "Codice padre",
                        "Macchina",
                        "Materiale",
                        "Denominazione profilo",
                        "Data di creazione",
                        "Nome",
                        "Codice",
                        "Cliente",
                        "Q.tà per Disegno",
                        "Misura di massima",
                        "Massa",
                        "Percorso"]
        self._data = tabella

    # Minimum necessary methods:
    def rowCount(self, parent):
        return len(self._data)

    def columnCount(self, parent):
        return len(self._headers)

    def data(self, index, role):
        # original if statement:
        # if role == qtc.Qt.DisplayRole:
        # Add EditRole so that the cell is not cleared when editing
        if role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
            return self._data[index.row()][index.column()]


    # Additional features methods:

    def getCell(self, X, Y):
        return self._data[X][Y]

    def NumbersOfRows(self):
        return len(self._data)

    def NumbersOfcolumn(self):
        return len(self._headers)

    def headerData(self, section, orientation, role):

        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._headers[section]
        else:
            return super().headerData(section, orientation, role)

    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()  # needs to be emitted before a sort
        self._data.sort(key=lambda x: x[column])
        if order == QtCore.Qt.DescendingOrder:
            self._data.reverse()
        self.layoutChanged.emit()  # needs to be emitted after a sort

    # Methods for Read/Write

    def flags(self, index):
        return super().flags(index) | QtCore.Qt.ItemIsEditable

    def setData(self, index, value, role):
        if index.isValid() and role == QtCore.Qt.EditRole:
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index, [role])
            return True
        else:
            return False
