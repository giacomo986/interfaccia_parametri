import sys, os
from PyQt5 import QtWidgets, QtCore
import interfaccia
import csv


class CsvTableModel(QtCore.QAbstractTableModel):
    """The model for a CSV table."""

    def __init__(self, csv_file):
        super().__init__()
        self.filename = csv_file
        with open(self.filename) as fh:
            csvreader = csv.reader(fh)
            self._headers = next(csvreader)
            self._data = list(csvreader)

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

    def rowNumber(self):
        return len(self._data)

    def columnNumber(self):
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

def InizializzaDati():
    modelClienti = CsvTableModel(cwd + "/clienti.csv")
    for element in range(0, modelClienti.rowNumber()):
        ui.comboBox_Cliente.addItem(modelClienti.getCell(element, 0), modelClienti.getCell(element, 1))
    
    modelMateriali = CsvTableModel(cwd + "/materiali.csv")
    for element in range(0, modelMateriali.rowNumber()):
        ui.comboBox_Materiale.addItem(modelMateriali.getCell(element, 0), modelMateriali.getCell(element, 1))

    ui.CancelButton.clicked.connect(ChiudiApplicazione)
    ui.AcceptButton.clicked.connect(SalvaDati)

def SalvaDati():
    print(ui.comboBox_Materiale.currentIndex() )
    print(ui.comboBox_Materiale.currentText() )
    print(ui.comboBox_Materiale.currentData() )
    modelFile = CsvTableModel(cwd + "/" + ui.lineEdit_Riferimento.text + ".csv")

def ChiudiApplicazione():
    QtCore.QCoreApplication.instance().quit()

if __name__ == "__main__":
    cwd = os.getcwd()
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = interfaccia.Ui_Form()
    ui.setupUi(Form)
    InizializzaDati()
    Form.show()
    sys.exit(app.exec_())