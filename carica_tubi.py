import sys, os
from PySide2 import QtWidgets, QtCore, QtGui
import resources.finestra_carica as interfaccia
import csv, datetime, Spreadsheet, json
#from resources.CsvTableModelClass import CsvTableModel

def ChiudiApplicazione():
    Form.close()

########################################
######## Punto d'ingresso macro ########
########################################

# Crea la finestra
Form = QtWidgets.QWidget()
ui = interfaccia.Ui_Form()
ui.setupUi(Form)
#InizializzaDati()
Form.show()