import resources.finestra_carica as interfaccia
from PySide2 import QtWidgets, QtCore, QtGui


# Crea la finestra
Form = QtWidgets.QWidget()
ui = interfaccia.Ui_Form()
ui.setupUi(Form)
Form.show()