import sys, os
from PySide2 import QtWidgets, QtCore, QtGui
import resources.finestra_carica as interfaccia
import csv, datetime, Spreadsheet, json
from resources.CsvTableModelClass import CsvTableModel
import resources.database.database as database

def InizializzaDati():

    ui.comboBox_Cliente.addItem("<Qualsiasi cliente>", False)
    clienti = leggiCSV(cwd + "/resources/clienti.csv")
    for element in clienti:
        ui.comboBox_Cliente.addItem(element[0], element[1])
    
    ui.comboBox_Materiale.addItem("<Qualsiasi materiale>", False)
    materiali = leggiCSV(cwd + "/resources/materiali.csv")
    for element in materiali:
        nome_materiale = element[0]
        peso_specifico = element[1]
        ui.comboBox_Materiale.addItem(nome_materiale + " (" + peso_specifico + " g/cm³)", peso_specifico)

    ui.CancelButton.clicked.connect(ChiudiApplicazione)
    ui.SearchButton.clicked.connect(recupera_dati)
    ui.AcceptButton.clicked.connect(carica_documento)

def leggiCSV(PercorsoFile):
    lista = []
    with open(PercorsoFile, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        next(reader)
        for row in reader:
            lista.append(row)
    return lista

def ChiudiApplicazione():
    Form.close()

def recupera_dati():
    global tabella
    connesso = database.connetti(cwd)
    if connesso:
        condizioni = leggi_campi(){ "riferimento" : "aaaa", "codice_padre" : "" }
        tabella = database.interroga_database(condizioni)
        database.disconnetti()
        model = CsvTableModel(tabella)
        ui.tableView.setModel(model)
    else:
        qm = QtWidgets.QMessageBox
        qm.information(None, "Database non raggiungibile", "Il database non è raggiungibile, assicurarsi che i dati di accesso siano corretti e che il database sia avviato.")
        return

def leggi_campi():
    dizionario = {"riferimento" : ui.lineEdit_Riferimento.text(),
                    "codice_padre" : ui.lineEdit_CodicePadre.text(),
                    "macchina" : ui.lineEdit_Macchina.text(),
                    "materiale" :
                    "denominazione_profilo" :
                    "data_creazione" :
                    "nome" :
                    "codice" :
                    "cliente" : 
                    "quantità_per_disegno" :
                    "misura_di_massima" :
                    "massa" :
    return dizionario

def carica_documento():
    #global tabella
    selected = ui.tableView.selectedIndexes()
    riga_selezionata = selected[0].row()
    percorso_file = tabella[riga_selezionata][12]

    if not selected:
        qm = QtWidgets.QMessageBox
        qm.information(None, "Nessun elemento selezionato", "Selezionare un elemento dalla tabella.")
        return
    
    if not os.path.exists(percorso_file):
        qm = QtWidgets.QMessageBox
        qm.information(None, "Percorso non valido", "Non è stato trovato il file indicato dal percorso. Il percorso potrebbe essere sbagliato o non raggiungibile.")
        return

    try:
        FreeCAD.openDocument(percorso_file)
        ChiudiApplicazione()
    except:
        qm = QtWidgets.QMessageBox
        qm.information(None, "Errore caricamento file", "Non è possibile caricare il file a cause di un errore sconosciuto.")
        return

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