import sys, os
from PySide2 import QtWidgets, QtCore, QtGui
import resources.finestra_salva as interfaccia
import resources.database.database as database
import csv, datetime, Spreadsheet, json

def InizializzaDati():

    clienti = leggiCSV(cwd + "/resources/clienti.csv")
    for element in clienti:
        ui.comboBox_Cliente.addItem(element[0], element[1])
    
    materiali = leggiCSV(cwd + "/resources/materiali.csv")
    for element in materiali:
        nome_materiale = element[0]
        peso_specifico = element[1]
        ui.comboBox_Materiale.addItem(nome_materiale + " (" + peso_specifico + " g/cm³)", peso_specifico)

    ui.comboBox_Materiale.currentIndexChanged.connect(impostaMassa)
    impostaMassa()
    
    ui.DateTimeEdit_Data.setDateTime(datetime.datetime.now())
    
    aggiungiBoundBox()
    
    ui.CancelButton.clicked.connect(ChiudiApplicazione)
    ui.AcceptButton.clicked.connect(SalvaDati)

def impostaMassa():
    peso_specifico = ui.comboBox_Materiale.currentData()
    ui.lineEdit_Massa.setText(str(calcolaMassa(peso_specifico)))

def calcolaMassa(peso_specifico):
    objs = FreeCADGui.Selection.getSelection()
    s = objs[0].Shape
    Volume = s.Volume # il volume è espresso in mm³
    Massa = round(float(peso_specifico) * (Volume / 1000.0), 3) # il peso specifico è espesso in g/cm³
    return Massa

def aggiungiBoundBox():
    objs = FreeCADGui.Selection.getSelection()
    s = objs[0].Shape
    boundBox_= s.BoundBox

    ui.comboBox_MisuraMax.addItem("lunghezza asse x: " + str(round(boundBox_.XLength, 3)), boundBox_.XLength)
    ui.comboBox_MisuraMax.addItem("lunghezza asse y: " + str(round(boundBox_.YLength, 3)), boundBox_.YLength)
    ui.comboBox_MisuraMax.addItem("lunghezza asse z: " + str(round(boundBox_.ZLength, 3)), boundBox_.ZLength)

def SalvaDati():
    if ui.lineEdit_Riferimento.text() == "":
        qm = QtWidgets.QMessageBox
        question = qm.information(None, 'Campo "Riferimento" vuoto', 'Il campo "Riferimento" è vuoto, riempire il campo "Riferimento" prima di confermare')
        return

    sheet = crea_spreadsheet()
    popola_spreadsheet(sheet)

    qm = QtWidgets.QMessageBox
    question = qm.question(None, "Esportazione in FCStd", "Si desidera esportare il disegno in formato FCStd?", qm.Yes | qm.No)
    if (question == qm.No):
        qm.information(None, "Informazione", "Nessuna esportazione")
    else:
        filePath = Percorso_disegni + ui.comboBox_Cliente.currentText() + "/"

        if not(ui.lineEdit_CodicePadre.text() == ""):
            filePath = filePath + ui.lineEdit_CodicePadre.text() + "/"

        os.makedirs(filePath, exist_ok=True)  # Crea la cartella se non esiste

        nomeFile = str(filePath + ui.lineEdit_Riferimento.text() + ".FCStd") # imposta il nome del file da salvare

        if not os.path.exists(nomeFile):
            open(nomeFile, "w")
        else:
            qm = QtWidgets.QMessageBox
            question = qm.question(None, "File già esistente", "File già esistente. Vuoi sovrascrivere il file?", qm.Yes | qm.No)
            if (question == qm.No):
                qm.information(None, "Informazione", "Nessuna modifica")

        Documento.saveAs(nomeFile)

        qm = QtWidgets.QMessageBox
        qm.information(None, "Informazione", "File salvato. Percorso: " + nomeFile)

    qm = QtWidgets.QMessageBox
    question = qm.question(None, "Salvataggio su database", "Si desidera salvare i dati su database?", qm.Yes | qm.No)
    if (question == qm.No):
        qm.information(None, "Informazione", "Nessuna aggiunta al database")
    else:
        connesso = database.connetti(cwd)
        if connesso:
            database.inserisci_riga((ui.lineEdit_Riferimento.text(),
                                    ui.lineEdit_CodicePadre.text(),
                                    u~~i.lineEdit_Macchina.text(),
                                    str(ui.comboBox_Materiale.currentData()),
                                    ui.comboBox_Denominazione.currentText(),
                                    ui.DateTimeEdit_Data.dateTime().toPython().strftime("%Y-%m-%d %H:%M:%S"),
                                    ui.lineEdit_Nome.text(),
                                    ui.lineEdit_Codice.text(),
                                    ui.comboBox_Cliente.currentText(),
                                    int(ui.lineEdit_Quantita.text()),
                                    ui.comboBox_MisuraMax.currentData(),
                                    float(ui.lineEdit_Massa.text()),
                                    nomeFile)
                                    )
            database.disconnetti()
        else:
            qm = QtWidgets.QMessageBox
            question = qm.information(None, "Database non raggiungibile", "Il database non è raggiungibile, assicurarsi che i dati di accesso siano corretti e che il database sia avviato.")
            return
    ChiudiApplicazione()

def leggiCSV(PercorsoFile):
    lista = []
    with open(PercorsoFile, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        next(reader)
        for row in reader:
            lista.append(row)

    return lista

def crea_spreadsheet():
    sheet = App.ActiveDocument.addObject("Spreadsheet::Sheet")
    sheet.Label = ui.lineEdit_Riferimento.text()
    return sheet

def popola_spreadsheet(sheet):
    sheet.set("A1", "Riferimento:")
    sheet.set("B1", ui.lineEdit_Riferimento.text())

    sheet.set("A2", "Codice padre:")
    sheet.set("B2", ui.lineEdit_CodicePadre.text())

    sheet.set("A3", "Macchina:")
    sheet.set("B3", ui.lineEdit_Macchina.text())

    sheet.set("A4", "Materiale:")
    sheet.set("B4", str(ui.comboBox_Materiale.currentData()))

    sheet.set("A5", "Denominazione profilo:")
    sheet.set("B5", ui.comboBox_Denominazione.currentText())

    sheet.set("A6", "Data di creazione:")
    sheet.set("B6", ui.DateTimeEdit_Data.dateTime().toPython().strftime("%Y-%m-%d %H:%M:%S"))

    sheet.set("A7", "Nome:")
    sheet.set("B7", ui.lineEdit_Nome.text())

    sheet.set("A8", "Codice:")
    sheet.set("B8", ui.lineEdit_Codice.text())
    sheet.set("B10", ui.lineEdit_Quantita.text())

    sheet.set("A11", "Misura di massima:")
    sheet.set("B11", str(ui.comboBox_MisuraMax.currentData()))

    sheet.set("A12", "Massa:")
    sheet.set("B12", ui.lineEdit_Massa.text())

    sheet.setAlignment("A1:A12", "right|vcenter|vimplied")
    sheet.setAlignment("B1:B20", "center|vcenter|vimplied")
    sheet.recompute()

def ChiudiApplicazione():
    Form.close()


########################################
######## Punto d'ingresso macro ########
########################################

# La macro comincia verificando se è stato selezionato un solido da cui estrapolare le dimensioni
objs = FreeCADGui.Selection.getSelection()
if len(objs) >= 1:
    if hasattr(objs[0], "Shape"): # Se il primo oggetto della selezione è un solido allora la macro richiama la finestra
        
        # Cerca la cartella dove sono situate le macro e salva il percorso.
        p = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Macro")
        cwd = p.GetString("MacroPath")

        # apre il file di configurazione che contiene il percorso di salvataggio dei disegni
        try:
            with open(cwd + "/resources/macro_config.json", "r") as read_file:
                config = json.load(read_file)
            Percorso_disegni = config["Percorso_disegni"]
        except:
            qm = QtWidgets.QMessageBox
            question = qm.information(None, "Errore file di configurazione", "File di configurazione non esistente o non leggibile.")
            return

        Documento =  App.ActiveDocument # Salva un riferimento del documento aperto per comodità

        # Crea la finestra
        Form = QtWidgets.QWidget()
        ui = interfaccia.Ui_Form()
        ui.setupUi(Form)
        InizializzaDati()
        Form.show()
    else:
        qm = QtWidgets.QMessageBox
        qm.information(None, "Nessun solido selezionato", "Per avviare la macro è necessario selezionare un solido")
else:
    qm = QtWidgets.QMessageBox
    qm.information(None, "Nessun solido selezionato", "Per avviare la macro è necessario selezionare un solido")