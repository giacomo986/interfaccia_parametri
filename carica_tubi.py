import sys, os
from PySide2 import QtWidgets, QtCore, QtGui
import resources.finestra_carica as interfaccia
import csv, datetime, Spreadsheet, json
from resources.CsvTableModelClass import CsvTableModel
import resources.database.database as database

def InizializzaDati():
    ui.CancelButton.clicked.connect(ChiudiApplicazione)
    ui.SearchButton.clicked.connect(recupera_dati)
    ui.AcceptButton.clicked.connect(carica_documento)

def ChiudiApplicazione():
    Form.close()

def recupera_dati():
    global tabella
    database.connetti(cwd)
    tabella = database.interroga_database()
    database.disconnetti()
    model = CsvTableModel(filename)
    self.tableview.setModel(self.model)

def carica_documento():
    global tabella
    FreeCAD.openDocument(tabella[1][13])
    ChiudiApplicazione()

########################################
######## Punto d'ingresso macro ########
########################################

p = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Macro")
cwd = p.GetString("MacroPath")

# Crea la finestra
Form = QtWidgets.QWidget()
ui = interfaccia.Ui_Form()
ui.setupUi(Form)
InizializzaDati()
Form.show()