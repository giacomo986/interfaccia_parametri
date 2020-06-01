import sys, os, csv, datetime, Spreadsheet, json
from PySide2 import QtWidgets, QtCore, QtGui

p = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Macro")
cwd = p.GetString("MacroPath")
sys.path.insert(1, cwd)

import resources.finestra_carica as interfaccia
from resources.CsvTableModelClass import CsvTableModel
import resources.database.database as database

def InizializzaIterfaccia():

    ui.comboBox_Cliente.addItem("<Qualsiasi cliente>", False)
    try:
        clienti = leggiCSV(cwd + "/resources/clienti.csv")
    except:
        qm = QtWidgets.QMessageBox
        qm.information(None, "Errore", "Lista clienti mancante o formattata male, controllare lista clienti al percorso: {}".format(cwd + "/resources/clienti.csv"))
        return False
    if not clienti:
        qm = QtWidgets.QMessageBox
        qm.information(None, "Errore", "Lista clienti vuota, popolare lista clienti nel percorso: {}".format(cwd + "/resources/clienti.csv"))
        return False
    for element in clienti:
        ui.comboBox_Cliente.addItem(element[0], element[1])
    
    ui.comboBox_Materiale.addItem("<Qualsiasi materiale>", False)
    try:
        materiali = leggiCSV(cwd + "/resources/materiali.csv")
    except:
        qm = QtWidgets.QMessageBox
        qm.information(None, "Errore", "Lista materiali mancante o formattata male, controllare lista materiali al percorso: {}".format(cwd + "/resources/materiali.csv"))
        return False
    if not materiali:
        qm = QtWidgets.QMessageBox
        qm.information(None, "Errore", "Lista materiali vuota, popolare lista materiali nel percorso: {}".format(cwd + "/resources/materiali.csv"))
        return False
    for element in materiali:
        nome_materiale = element[0]
        peso_specifico = element[1]
        ui.comboBox_Materiale.addItem(nome_materiale + " (" + peso_specifico + " g/cm³)", peso_specifico)

    ui.comboBox_Denominazione.addItem("<Qualsiasi denominazione>", False)
    try:
        denominazioni = leggiCSV(cwd + "/resources/denominazioni_profilo.csv")
    except:
        qm = QtWidgets.QMessageBox
        qm.information(None, "Errore", "Lista denominazioni o formattata male, controllare lista denominazioni al percorso: {}".format(cwd + "/resources/denominazioni_profilo.csv"))
        return False
    if not denominazioni:
        qm = QtWidgets.QMessageBox
        qm.information(None, "Errore", "Lista denominazioni vuota, popolare lista denominazioni nel percorso: {}".format(cwd + "/resources/denominazioni_profilo.csv"))
        return False
    for element in denominazioni:
        ui.comboBox_Denominazione.addItem(element[0], element[1])

    ui.DateTimeEdit_Data2.setDateTime(datetime.datetime.now())

    ui.CancelButton.clicked.connect(ChiudiApplicazione)
    ui.SearchButton.clicked.connect(recupera_dati)
    ui.AcceptButton.clicked.connect(carica_documento)
    return True

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
        #condizioni = {"p.riferimento" : [[ "%%%s%%" % ui.lineEdit_Riferimento.text(), "LIKE"]]}
        condizioni = leggi_campi()
        tabella = database.interroga_tabella_parti(condizioni)
        database.disconnetti()
        model = CsvTableModel(tabella)
        ui.tableView.setModel(model)
    else:
        qm = QtWidgets.QMessageBox
        qm.information(None, "Database non raggiungibile", "Il database non è raggiungibile, assicurarsi che i dati di accesso siano corretti e che il database sia avviato.")
        return

def leggi_campi():
    # viene creato un dizionario per i filtri per la query del database
    dizionario = {"p.riferimento" : [["" if not ui.lineEdit_Riferimento.text() else "%%%s%%" % ui.lineEdit_Riferimento.text(), "LIKE"]],
                    "a.codice_padre" : [["" if not ui.lineEdit_CodicePadre.text() else "%%%s%%" % ui.lineEdit_CodicePadre.text(), "LIKE"]],
                    "p.macchina" : [["" if not ui.lineEdit_Macchina.text() else "%%%s%%" % ui.lineEdit_Macchina.text(), "LIKE"]],
                    "p.materiale" : [[str(ui.comboBox_Materiale.currentData()), "="]] if not ui.comboBox_Materiale.currentText() == "<Qualsiasi materiale>" else [["", "="]],
                    "p.denominazione_profilo" : [[ui.comboBox_Denominazione.currentText(), "="]] if not ui.comboBox_Denominazione.currentText() == "<Qualsiasi denominazione>" else [["", "="]],
                    "p.data_creazione" : [[ui.DateTimeEdit_Data.dateTime().toPython().strftime("%Y-%m-%d %H:%M:%S"), ">="], [ui.DateTimeEdit_Data2.dateTime().toPython().strftime("%Y-%m-%d %H:%M:%S"), "<="]],
                    "p.nome" : [["" if not ui.lineEdit_Nome.text() else "%%%s%%" % ui.lineEdit_Nome.text(), "LIKE"]],
                    "p.codice" : [["" if not ui.lineEdit_Codice.text() else "%%%s%%" % ui.lineEdit_Codice.text(), "LIKE"]],
                    "p.cliente" : [[ui.comboBox_Cliente.currentText(), "="]] if not ui.comboBox_Cliente.currentText() == "<Qualsiasi cliente>" else [["", "="]],
                    "p.quantità_per_disegno" : [[ui.lineEdit_Quantita.text(), "="]],
                    "p.misura_di_massima" : [[ui.lineEdit_MisuraMax.text(), ">="], [ui.lineEdit_MisuraMax2.text(), "<="]],
                    "p.massa" : [[ui.lineEdit_Massa.text(), ">="], [ui.lineEdit_Massa2.text(), "<="]]
                    }
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
tutto_ok = InizializzaIterfaccia()
if tutto_ok:
    Form.show()