import sys, os
from PySide2 import QtWidgets, QtCore, QtGui
import resources.interfaccia as interfaccia
import csv, datetime, Spreadsheet
from resources.CsvTableModelClass import CsvTableModel

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
    question = qm.question(None, "Esportazione in CSV", "Si desidera esportare in dati in formato CSV?", qm.Yes | qm.No)
    if (question == qm.No):
        qm.information(None, "Informazione", "Nessuna esportazione")
    else:
        filePath = cwd + "/resources/" + ui.comboBox_Cliente.currentText()

        os.makedirs(filePath, exist_ok=True)  # Crea la cartella se non esiste

        nomeFile = str(filePath + "/" + ui.lineEdit_Riferimento.text() + ".csv") # imposta il nome del file da salvare

        if not os.path.exists(nomeFile):
            open(nomeFile, "w")
        else:
            qm = QtWidgets.QMessageBox
            question = qm.question(None, "File già esistente", "File già esistente. Vuoi sovrascrivere il file?", qm.Yes | qm.No)
            if (question == qm.No):
                qm.information(None, "Informazione", "Nessuna modifica")

        scriviCSV(nomeFile)

        qm = QtWidgets.QMessageBox
        qm.information(None, "Informazione", "File salvato. Percorso: " + nomeFile)

    qm = QtWidgets.QMessageBox
    question = qm.question(None, "Salvataggio su database", "Si desidera salvare i dati su database?", qm.Yes | qm.No)
    if (question == qm.No):
        qm.information(None, "Informazione", "Nessuna aggiunta al database")
    else:
        import resources.database.database as database
        database.connetti(cwd)
        database.inserisci_riga((ui.lineEdit_Riferimento.text(),
                                ui.lineEdit_CodicePadre.text(),
                                ui.lineEdit_Macchina.text(),
                                ui.comboBox_Materiale.currentText(),
                                ui.comboBox_Denominazione.currentText(),
                                ui.DateTimeEdit_Data.dateTime().toPython().strftime("%Y-%m-%d %H:%M:%S"),
                                ui.lineEdit_Nome.text(),
                                ui.lineEdit_Codice.text(),
                                ui.comboBox_Cliente.currentText(),
                                int(ui.lineEdit_Quantita.text()),
                                ui.comboBox_MisuraMax.currentData(),
                                float(ui.lineEdit_Massa.text()),
                                str(cwd + "/resources/" + ui.comboBox_Cliente.currentText() + "/" + ui.lineEdit_Riferimento.text() + ".csv"))
                                )

    ChiudiApplicazione()

def scriviCSV(PercorsoFile):
    with open(PercorsoFile, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(["Riferimento"] +
                        ["Codice padre"] +
                        ["Macchina"] +
                        ["Materiale"] +
                        ["Denominazione profilo"] +
                        ["Data di creazione"] +
                        ["Nome"] +
                        ["Codice"] +
                        ["Cliente"] +
                        ["Q.tà per Disegno"] +
                        ["Misura di massima"] +
                        ["Massa"])

        writer.writerow([ui.lineEdit_Riferimento.text()] +
                        [ui.lineEdit_CodicePadre.text()] +
                        [ui.lineEdit_Macchina.text()] +
                        [ui.comboBox_Materiale.currentText()] +
                        [ui.comboBox_Denominazione.currentText()] +
                        [ui.DateTimeEdit_Data.dateTime().toPython().strftime("%Y-%m-%d %H:%M:%S")] +
                        [ui.lineEdit_Nome.text()] +
                        [ui.lineEdit_Codice.text()] +
                        [ui.comboBox_Cliente.currentText()] +
                        [ui.lineEdit_Quantita.text()] +
                        [ui.comboBox_MisuraMax.currentData()] +
                        [ui.lineEdit_Massa.text()])

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
    sheet.set("B4", ui.comboBox_Materiale.currentText())

    sheet.set("A5", "Denominazione profilo:")
    sheet.set("B5", ui.comboBox_Denominazione.currentText())

    sheet.set("A6", "Data di creazione:")
    sheet.set("B6", ui.DateTimeEdit_Data.dateTime().toPython().strftime("%Y-%m-%d %H:%M:%S"))

    sheet.set("A7", "Nome:")
    sheet.set("B7", ui.lineEdit_Nome.text())

    sheet.set("A8", "Codice:")
    sheet.set("B8", ui.lineEdit_Codice.text())

    sheet.set("A9", "Cliente:")
    sheet.set("B9", ui.comboBox_Cliente.currentText())

    sheet.set("A10", "Q.tà per Disegno:")
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
        p = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Macro")
        cwd = p.GetString("MacroPath")
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