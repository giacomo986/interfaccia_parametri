import sys, os, csv, datetime, Spreadsheet, json
from PySide2 import QtWidgets, QtCore, QtGui

p = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Macro")
cwd = p.GetString("MacroPath")
sys.path.insert(1, cwd)

import resources.finestra_salva as interfaccia
import resources.database.database as database

def InizializzaIterfaccia():

    clienti = leggiCSV(cwd + "/resources/clienti.csv")
    for element in clienti:
        ui.comboBox_Cliente.addItem(element[0], element[1])
    
    materiali = leggiCSV(cwd + "/resources/materiali.csv")
    for element in materiali:
        nome_materiale = element[0]
        peso_specifico = element[1]
        ui.comboBox_Materiale.addItem("%s (%s g/cm³)" % (nome_materiale, peso_specifico), {"nome" : nome_materiale, "peso_specifico" : peso_specifico})

    denominazioni = leggiCSV(cwd + "/resources/denominazioni_profilo.csv")
    for element in denominazioni:
        ui.comboBox_Denominazione.addItem(element[0], element[1])

    ui.comboBox_Materiale.currentIndexChanged.connect(impostaMassa)
    impostaMassa()

    ui.DateTimeEdit_Data.setDateTime(datetime.datetime.now())
    
    ui.DateTimeEdit_ultima_modifica.setDateTime(datetime.datetime.now())
    
    aggiungiBoundBox()

    ui.CancelButton.clicked.connect(ChiudiApplicazione)
    ui.AcceptButton.clicked.connect(SalvaDati)

def impostaMassa():
    peso_specifico = ui.comboBox_Materiale.currentData()["peso_specifico"]
    ui.lineEdit_Massa.setText(str(calcolaMassa(peso_specifico)))

def calcolaMassa(peso_specifico):
    s = oggetto_selezionato.Shape
    Volume = s.Volume # il volume è espresso in mm³
    Massa = round(float(peso_specifico) * (Volume / 1000.0), 3) # il peso specifico è espesso in g/cm³
    return Massa

def aggiungiBoundBox():
    s = oggetto_selezionato.Shape
    boundBox_= s.BoundBox

    ui.comboBox_MisuraMax.addItem("lunghezza asse x: " + str(round(boundBox_.XLength, 3)), boundBox_.XLength)
    ui.comboBox_MisuraMax.addItem("lunghezza asse y: " + str(round(boundBox_.YLength, 3)), boundBox_.YLength)
    ui.comboBox_MisuraMax.addItem("lunghezza asse z: " + str(round(boundBox_.ZLength, 3)), boundBox_.ZLength)

def esporta_e_linka():
    selectedObjs = FreeCADGui.Selection.getSelection()[0]

    nome = selectedObjs.Label

    Documento_originale = FreeCAD.ActiveDocument

    Documento_nuovo = FreeCAD.newDocument(nome)

    Documento_nuovo.saveAs("/home/giacomo/%s.FCStd" % nome)

    corpo = Documento_nuovo.moveObject(selectedObjs, True)

    Documento_nuovo.saveAs("/home/giacomo/%s.FCStd" % nome)

    Documento_originale.addObject('App::Link',nome).setLink(corpo)
    pass

def SalvaDati():
    if ui.lineEdit_Riferimento.text() == "":
        qm = QtWidgets.QMessageBox
        question = qm.information(None, 'Campo "Riferimento" vuoto', 'Il campo "Riferimento" è vuoto, riempire il campo "Riferimento" prima di confermare')
        return

    Documento_nuovo = FreeCAD.newDocument(ui.lineEdit_Riferimento.text())
    corpo = Documento_nuovo.copyObject(oggetto_selezionato, True)
    corpo.Label = ui.lineEdit_Riferimento.text()
    if ui.lineEdit_CodicePadre.text():
        Parte = Documento_nuovo.addObject('App::Part', ui.lineEdit_CodicePadre.text())
        Parte.addObject(corpo)
    
    FreeCAD.setActiveDocument(ui.lineEdit_Riferimento.text())

    filePath = Percorso_disegni + ui.comboBox_Cliente.currentText() + "/"

    if not(ui.lineEdit_CodicePadre.text() == ""):
        filePath = filePath + ui.lineEdit_CodicePadre.text() + "/"

    os.makedirs(filePath, exist_ok=True)  # Crea la cartella se non esiste

    nomeFile = str("%s%s.FCStd" % (filePath, ui.lineEdit_Riferimento.text())) # imposta il nome del file da salvare


    # Si connette al database, verifica che il file non sia già esistente e salva i dati con il percorso
    connesso = database.connetti(cwd)
    if connesso:

        condizione_assieme = ui.lineEdit_CodicePadre.text()
        assieme_esistente = database.interroga_tabella_parti(condizione_assieme)

        if assieme_esistente:
            pass
        else:
            database.inserisci_riga_assiemi((ui.lineEdit_CodicePadre.text(),
                                            ui.lineEdit_Macchina.text(),
                                            ui.DateTimeEdit_Data.dateTime().toPython().strftime("%Y-%m-%d %H:%M:%S"),
                                            ui.DateTimeEdit_ultima_modifica.dateTime().toPython().strftime("%Y-%m-%d %H:%M:%S"),
                                            ui.lineEdit_Codice.text(),
                                            nomeFile))

        condizione_parte = ui.lineEdit_Riferimento.text()
        disegno_esistente = database.interroga_tabella_parti(condizione_parte)

        if disegno_esistente:
            print("disegno esistente: %s" % disegno_esistente)
            pass
        else:
            database.inserisci_riga_parti((ui.lineEdit_Riferimento.text(),
                                        ui.lineEdit_CodicePadre.text(),
                                        ui.lineEdit_Macchina.text(),
                                        ui.comboBox_Materiale.currentData()["nome"],
                                        ui.comboBox_Denominazione.currentText(),
                                        ui.DateTimeEdit_Data.dateTime().toPython().strftime("%Y-%m-%d %H:%M:%S"),
                                        ui.DateTimeEdit_ultima_modifica.dateTime().toPython().strftime("%Y-%m-%d %H:%M:%S"),
                                        ui.lineEdit_Nome.text(),
                                        ui.lineEdit_Codice.text(),
                                        ui.comboBox_Cliente.currentText(),
                                        int(ui.lineEdit_Quantita.text()),
                                        ui.comboBox_MisuraMax.currentData(),
                                        float(ui.lineEdit_Massa.text()),
                                        nomeFile))
        database.disconnetti()
    else:
        qm = QtWidgets.QMessageBox
        question = qm.information(None, "Database non raggiungibile", "Il database non è raggiungibile, assicurarsi che i dati di accesso siano corretti e che il database sia avviato.")
        return


    sheet = crea_spreadsheet()
    popola_spreadsheet(sheet)

    if ui.lineEdit_CodicePadre.text():
        Parte.addObject(sheet)

    if os.path.exists(nomeFile):
        qm = QtWidgets.QMessageBox
        question = qm.question(None, "File già esistente", "File già esistente. Vuoi sovrascrivere il file?", qm.Yes | qm.No)
        if (question == qm.No):
            qm.information(None, "Informazione", "Nessuna modifica")
        else:
            Documento_nuovo.saveAs(nomeFile)
            qm = QtWidgets.QMessageBox
            qm.information(None, "Informazione", "File salvato. Percorso: " + nomeFile)
    else:
        Documento_nuovo.saveAs(nomeFile)
        qm = QtWidgets.QMessageBox
        qm.information(None, "Informazione", "File salvato. Percorso: " + nomeFile)

    FreeCAD.closeDocument(ui.lineEdit_Riferimento.text())

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
    sheet = FreeCAD.ActiveDocument.addObject("Spreadsheet::Sheet")
    sheet.Label = "SS_%s" % ui.lineEdit_Riferimento.text()
    return sheet

def popola_spreadsheet(sheet):
    sheet.set("A1", "Riferimento:")
    sheet.set("B1", ui.lineEdit_Riferimento.text())

    sheet.set("A2", "Codice padre:")
    sheet.set("B2", ui.lineEdit_CodicePadre.text())

    sheet.set("A3", "Macchina:")
    sheet.set("B3", ui.lineEdit_Macchina.text())

    sheet.set("A4", "Materiale:")
    sheet.set("B4", str(ui.comboBox_Materiale.currentData()["nome"]))

    sheet.set("A5", "Denominazione profilo:")
    sheet.set("B5", ui.comboBox_Denominazione.currentText())

    sheet.set("A6", "Data di creazione:")
    sheet.set("B6", ui.DateTimeEdit_Data.dateTime().toPython().strftime("%Y-%m-%d %H:%M:%S"))

    sheet.set("A7", "Data ultima modifica:")
    sheet.set("B7", ui.DateTimeEdit_Data.dateTime().toPython().strftime("%Y-%m-%d %H:%M:%S"))

    sheet.set("A8", "Nome:")
    sheet.set("B8", ui.lineEdit_Nome.text())

    sheet.set("A9", "Codice:")
    sheet.set("B9", ui.lineEdit_Codice.text())

    sheet.set("A10", "Cliente:")
    sheet.set("B10", ui.comboBox_Cliente.currentText())

    sheet.set("A11", "Quantità:")
    sheet.set("B11", ui.lineEdit_Quantita.text())

    sheet.set("A12", "Misura di massima:")
    sheet.set("B12", str(ui.comboBox_MisuraMax.currentData()))

    sheet.set("A13", "Massa:")
    sheet.set("B13", ui.lineEdit_Massa.text())

    sheet.setAlignment("A1:A13", "right|vcenter|vimplied")
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
    oggetto_selezionato = objs[0]
    if hasattr(oggetto_selezionato, "Shape"): # Se il primo oggetto della selezione è un solido allora la macro richiama la finestra
        # apre il file di configurazione che contiene il percorso di salvataggio dei disegni
        try:
            with open("%s/resources/macro_config.json" % cwd, "r") as read_file:
                config = json.load(read_file)
            Percorso_disegni = config["Percorso_disegni"]

            Documento_originale = FreeCAD.ActiveDocument # Salva un riferimento del documento originale aperto per comodità
        
            # Crea la finestra
            Form = QtWidgets.QWidget()
            ui = interfaccia.Ui_Form()
            ui.setupUi(Form)
            InizializzaIterfaccia()
            Form.show()
        except:
            qm = QtWidgets.QMessageBox
            question = qm.information(None, "Errore file di configurazione", "File di configurazione non esistente o non leggibile.")
    else:
        qm = QtWidgets.QMessageBox
        qm.information(None, "Nessun solido selezionato", "Per avviare la macro è necessario selezionare un solido")
else:
    qm = QtWidgets.QMessageBox
    qm.information(None, "Nessun solido selezionato", "Per avviare la macro è necessario selezionare un solido")