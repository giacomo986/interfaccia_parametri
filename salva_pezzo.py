import sys, os, csv, datetime, Spreadsheet, json, re
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Qt

p = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Macro")
cwd = p.GetString("MacroPath")
sys.path.insert(1, cwd)

import resources.finestra_salva as interfaccia
import resources.database.database as database

def InizializzaIterfaccia():
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
        ui.comboBox_Materiale.addItem("{0} ({1} g/cm³)".format(nome_materiale, peso_specifico), {"nome" : nome_materiale, "peso_specifico" : peso_specifico})

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

    ui.comboBox_Materiale.currentIndexChanged.connect(impostaMassa)
    impostaMassa()

    ui.DateTimeEdit_Data.setDateTime(datetime.datetime.now())
    
    ui.DateTimeEdit_ultima_modifica.setDateTime(datetime.datetime.now())
    
    aggiungiBoundBox()

    ui.CancelButton.clicked.connect(ChiudiApplicazione)
    ui.AcceptButton.clicked.connect(SalvaDati)
    return True

def leggiCSV(PercorsoFile):
    lista = []
    with open(PercorsoFile, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        next(reader)
        for row in reader:
            lista.append(row)
    return lista

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

def esporta(Documento_nuovo, Oggetto, Percorso, Riferimento, Codice_Padre):
    Oggetto.Label = Riferimento

    #Documento_nuovo.saveAs(Percorso)

    corpo = Documento_nuovo.copyObject(Oggetto, True)

    if Codice_Padre:
        Parte = Documento_nuovo.addObject('App::Part', Codice_Padre)
        Parte.addObject(corpo)
    
    sheet = crea_spreadsheet()
    popola_spreadsheet(sheet)

    if Codice_Padre:
        Parte.addObject(sheet)

    Documento_nuovo.saveAs(Percorso)
    #Documento_originale.addObject('App::Link', Riferimento).setLink(corpo)

    qm = QtWidgets.QMessageBox
    qm.information(None, "Informazione", "File salvato. Percorso: " + Percorso)

def verifica_formattazione_riferimento(riferimento):
    pattern = re.compile("(.+_[Rr][0-9]+)")
    if pattern.match(riferimento):
        return True
    return False

def SalvaDati():
    riferimento = ui.lineEdit_Riferimento.text()
    codice_padre = ui.lineEdit_CodicePadre.text()

    if riferimento == "":
        qm = QtWidgets.QMessageBox
        info = qm.information(None, 'Campo "Riferimento" vuoto', 'Il campo "Riferimento" è vuoto, riempire il campo "Riferimento" prima di confermare')
        return

    if Formattazione_rif:
        formattazione_riferimento = verifica_formattazione_riferimento(riferimento)
        if not formattazione_riferimento:
            qm = QtWidgets.QMessageBox
            info = qm.information(None, 'Campo "Riferimento" scritto male', 'Il campo "Riferimento" non è formattato nel modo corretto. Bisogna formattare il nome nel seguente modo: \nnomedelriferimento_rxxx \ndove xxx = numero della revisione')
            return

    filePath = Percorso_disegni + ui.comboBox_Cliente.currentText() + "/"

    if codice_padre:
        filePath = filePath + codice_padre + "/"

    nomeFile = str("{0}{1}.FCStd".format(filePath, riferimento)) # imposta il nome del file da salvare
    
    if os.path.exists(nomeFile):
        qm = QtWidgets.QMessageBox
        question = qm.question(None, "File già esistente", "File già esistente. Vuoi sovrascrivere il file?", qm.Yes | qm.No)
        if (question == qm.No):
            return

    os.makedirs(filePath, exist_ok=True)  # Crea la cartella se non esiste

    Documento_nuovo = FreeCAD.newDocument(riferimento)
    
    esporta(Documento_nuovo,
            oggetto_selezionato,
            nomeFile,
            riferimento,
            codice_padre)
    
    # Si connette al database, verifica che il file non sia già esistente e salva i dati con il percorso
    connesso = database.connetti(cwd)
    if connesso:

        condizione_assieme = codice_padre
        assieme_esistente = database.trova_id_assieme(condizione_assieme)

        if assieme_esistente:
            print("assieme esistente: {}".format(assieme_esistente))
            #TODO: scrivere funzione di aggiornamento assieme database
            pass
        else:
            database.inserisci_riga_assiemi((codice_padre,
                                            ui.lineEdit_Macchina.text(),
                                            ui.DateTimeEdit_Data.dateTime().toPython().strftime("%Y-%m-%d %H:%M:%S"),
                                            ui.DateTimeEdit_ultima_modifica.dateTime().toPython().strftime("%Y-%m-%d %H:%M:%S"),
                                            ui.comboBox_Cliente.currentText(),
                                            nomeFile))

        disegno_esistente = database.trova_id_parte(riferimento)

        if disegno_esistente:
            print("disegno esistente: {}".format(disegno_esistente))
            #TODO: scrivere funzione di aggiornamento parte database
            pass
        else:
            database.inserisci_riga_parti((riferimento,
                                        codice_padre,
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

    ChiudiApplicazione()

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

# classe derivata da QWidget per aggiungere evento di tasto premuto
class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.chiudi()

    def chiudi(self):
        print("Premuto il tasto Escape. Chiudo la finestra.")
        self.close()

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
            with open("{}/resources/macro_config.json".format(cwd), "r") as read_file:
                config = json.load(read_file)
            Percorso_disegni = config["Percorso_disegni"]
            Formattazione_rif = config["Formattazione_riferimento"]

            Documento_originale = FreeCAD.ActiveDocument # Salva un riferimento del documento originale aperto per comodità
        
            # Crea la finestra
            #Form = QtWidgets.QWidget()
            Form = MainWindow()
            ui = interfaccia.Ui_Form()
            ui.setupUi(Form)
            tutto_ok = InizializzaIterfaccia()
            if tutto_ok:
                Form.show()
        except:
            qm = QtWidgets.QMessageBox
            question = qm.information(None, "Errore di inizializzaione", "Possibili problemi di inizializzazione: file di configurazione mancante o scritto male.")
    else:
        qm = QtWidgets.QMessageBox
        qm.information(None, "Nessun solido selezionato", "Per avviare la macro è necessario selezionare un solido")
else:
    qm = QtWidgets.QMessageBox
    qm.information(None, "Nessun solido selezionato", "Per avviare la macro è necessario selezionare un solido")