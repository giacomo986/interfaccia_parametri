import sys, os, csv, datetime, Spreadsheet, json
from PySide2 import QtWidgets, QtCore, QtGui

p = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Macro")
cwd = p.GetString("MacroPath")
sys.path.insert(1, cwd)

import resources.finestra_carica as interfaccia
from resources.CsvTableModelClass import CsvTableModel
import resources.database.database as database

import resources.finestra_salva as finestra_modifica

def InizializzaIterfaccia():
    ui.label_anteprima.setPixmap(immagine_predefinita)  

    ui.comboBox_Cliente.addItem("<Qualsiasi cliente>", False)
    try:
        clienti = leggiCSV(cwd + "/resources/clienti.csv")
    except:
        qm = QtWidgets.QMessageBox
        qm.information(None, "Errore", f"Lista clienti mancante o formattata male, controllare lista clienti al percorso: {cwd}/resources/clienti.csv")
        return False
    if not clienti:
        qm = QtWidgets.QMessageBox
        qm.information(None, "Errore", f"Lista clienti vuota, popolare lista clienti nel percorso: {cwd}/resources/clienti.csv")
        return False
    for element in clienti:
        ui.comboBox_Cliente.addItem(element[0], element[1])
    
    ui.comboBox_Materiale.addItem("<Qualsiasi materiale>", False)
    try:
        materiali = leggiCSV(cwd + "/resources/materiali.csv")
    except:
        qm = QtWidgets.QMessageBox
        qm.information(None, "Errore", f"Lista materiali mancante o formattata male, controllare lista materiali al percorso: {cwd}/resources/materiali.csv")
        return False
    if not materiali:
        qm = QtWidgets.QMessageBox
        qm.information(None, "Errore", f"Lista materiali vuota, popolare lista materiali nel percorso: {cwd}/resources/materiali.csv")
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
        qm.information(None, "Errore", f"Lista denominazioni o formattata male, controllare lista denominazioni al percorso: {cwd}/resources/denominazioni_profilo.csv")
        return False
    if not denominazioni:
        qm = QtWidgets.QMessageBox
        qm.information(None, "Errore", f"Lista denominazioni vuota, popolare lista denominazioni nel percorso: {cwd}/resources/denominazioni_profilo.csv")
        return False
    for element in denominazioni:
        ui.comboBox_Denominazione.addItem(element[0], element[1])

    ui.DateTimeEdit_Data2.setDateTime(datetime.datetime.now())
    ui.DateTimeEdit_ultima_modifica2.setDateTime(datetime.datetime.now())

    ui.CancelButton.clicked.connect(ChiudiApplicazione)
    ui.SearchButton.clicked.connect(recupera_dati)
    ui.AcceptButton.clicked.connect(carica_documento)
    ui.ModifyButton.clicked.connect(modifica_riga)
    ui.DeleteButton.clicked.connect(elimina_riga)
    ui.tableView.clicked.connect(aggiorna_anteprima)
    return True

def Inizializza_iterfaccia_modifica():
    ui_modifica.lineEdit_Riferimento.setReadOnly(True)
    try:
        clienti = leggiCSV(cwd + "/resources/clienti.csv")
    except:
        qm = QtWidgets.QMessageBox
        qm.information(None, "Errore", f"Lista clienti mancante o formattata male, controllare lista clienti al percorso: {cwd}/resources/clienti.csv")
        return False
    if not clienti:
        qm = QtWidgets.QMessageBox
        qm.information(None, "Errore", f"Lista clienti vuota, popolare lista clienti nel percorso: {cwd}/resources/clienti.csv")
        return False
    for elemento in clienti:
        ui_modifica.comboBox_Cliente.addItem(elemento[0], elemento[1])
    
    try:
        materiali = leggiCSV(cwd + "/resources/materiali.csv")
    except:
        qm = QtWidgets.QMessageBox
        qm.information(None, "Errore", f"Lista materiali mancante o formattata male, controllare lista materiali al percorso: {cwd}/resources/materiali.csv")
        return False
    if not materiali:
        qm = QtWidgets.QMessageBox
        qm.information(None, "Errore", f"Lista materiali vuota, popolare lista materiali nel percorso: {cwd}/resources/materiali.csv")
        return False
    for elemento in materiali:
        nome_materiale = elemento[0]
        peso_specifico = elemento[1]
        ui_modifica.comboBox_Materiale.addItem(f"{nome_materiale} ({peso_specifico} g/cm³)", {"nome" : nome_materiale, "peso_specifico" : peso_specifico})
    
    try:
        denominazioni = leggiCSV(cwd + "/resources/denominazioni_profilo.csv")
    except:
        qm = QtWidgets.QMessageBox
        qm.information(None, "Errore", f"Lista denominazioni o formattata male, controllare lista denominazioni al percorso: {cwd}/resources/denominazioni_profilo.csv")
        return False
    if not denominazioni:
        qm = QtWidgets.QMessageBox
        qm.information(None, "Errore", f"Lista denominazioni vuota, popolare lista denominazioni nel percorso: {cwd}/resources/denominazioni_profilo.csv")
        return False
    for elemento in denominazioni:
        ui_modifica.comboBox_Denominazione.addItem(elemento[0], elemento[1])
        
    ui_modifica.DateTimeEdit_Data.setReadOnly(True)
    ui_modifica.DateTimeEdit_ultima_modifica.setReadOnly(True)
    
    ui_modifica.CancelButton.clicked.connect(Chiudi_iterfaccia_modifica)
    ui_modifica.AcceptButton.clicked.connect(Modifica_dati)

def Modifica_dati():
    global tabella
    if database.connetti(cwd):
        dati = (ui_modifica.lineEdit_Riferimento.text(),
                ui_modifica.lineEdit_CodicePadre.text(),
                ui_modifica.lineEdit_Macchina.text(),
                ui_modifica.comboBox_Materiale.currentData()["nome"],
                ui_modifica.comboBox_Denominazione.currentText(),
                ui_modifica.DateTimeEdit_Data.dateTime().toPython().strftime("%Y-%m-%d %H:%M:%S"),
                ui_modifica.DateTimeEdit_ultima_modifica.dateTime().toPython().strftime("%Y-%m-%d %H:%M:%S"),
                ui_modifica.lineEdit_Nome.text(),
                ui_modifica.lineEdit_Codice.text(),
                ui_modifica.comboBox_Cliente.currentText(),
                int(ui_modifica.lineEdit_Quantita.text()),
                ui_modifica.comboBox_MisuraMax.currentData(),
                float(ui_modifica.lineEdit_Massa.text())
                )
        if database.aggiorna_riga_parti(dati):
            print("Aggiornamento avvenuto con successo")
        database.disconnetti()
    else:
        qm = QtWidgets.QMessageBox
        qm.information(None, "Database non raggiungibile", "Il database non è raggiungibile, assicurarsi che i dati di accesso siano corretti e che il database sia avviato.")
    Chiudi_iterfaccia_modifica()

def Chiudi_iterfaccia_modifica():
    Form_modifica.close()

def Carica_dati_iterfaccia_modifica(riga_selezionata = []):
    #print(riga_selezionata)
    ui_modifica.lineEdit_Riferimento.setText(str(riga_selezionata[0]))
    ui_modifica.lineEdit_CodicePadre.setText(str(riga_selezionata[1]))
    ui_modifica.lineEdit_Macchina.setText(str(riga_selezionata[2]))
    
    Index_Materiale = ui_modifica.comboBox_Materiale.findText(riga_selezionata[3], QtCore.Qt.MatchFixedString)
    if Index_Materiale >= 0:
         ui_modifica.comboBox_Materiale.setCurrentIndex(Index_Materiale)
    
    Index_Denominazione = ui_modifica.comboBox_Denominazione.findText(riga_selezionata[4], QtCore.Qt.MatchFixedString)
    if Index_Denominazione >= 0:
         ui_modifica.comboBox_Denominazione.setCurrentIndex(Index_Denominazione)

    ui_modifica.DateTimeEdit_Data.setDateTime(riga_selezionata[5])
    ui_modifica.DateTimeEdit_ultima_modifica.setDateTime(datetime.datetime.now())
    ui_modifica.lineEdit_Nome.setText(str(riga_selezionata[7]))
    ui_modifica.lineEdit_Codice.setText(str(riga_selezionata[8]))
    
    Index_Cliente = ui_modifica.comboBox_Cliente.findText(riga_selezionata[9], QtCore.Qt.MatchFixedString)
    if Index_Cliente >= 0:
         ui_modifica.comboBox_Cliente.setCurrentIndex(Index_Cliente)

    ui_modifica.lineEdit_Quantita.setText(str(riga_selezionata[10]))
    ui_modifica.comboBox_MisuraMax.addItem("lunghezza: " + str(round(riga_selezionata[11], 3)), riga_selezionata[11])
    ui_modifica.lineEdit_Massa.setText(str(riga_selezionata[12]))

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
    dizionario = {"p.riferimento" : [["" if not ui.lineEdit_Riferimento.text() else f"%%{ui.lineEdit_Riferimento.text()}%%", "LIKE"]],
                    "p.codice_padre" : [["" if not ui.lineEdit_CodicePadre.text() else f"%%{ui.lineEdit_CodicePadre.text()}%%", "LIKE"]],
                    "p.macchina" : [["" if not ui.lineEdit_Macchina.text() else f"%%{ui.lineEdit_Macchina.text()}%%", "LIKE"]],
                    "p.materiale" : [[str(ui.comboBox_Materiale.currentData()), "="]] if not ui.comboBox_Materiale.currentText() == "<Qualsiasi materiale>" else [["", "="]],
                    "p.denominazione_profilo" : [[ui.comboBox_Denominazione.currentText(), "="]] if not ui.comboBox_Denominazione.currentText() == "<Qualsiasi denominazione>" else [["", "="]],
                    "p.data_creazione" : [[ui.DateTimeEdit_Data.dateTime().toPython().strftime("%Y-%m-%d %H:%M:%S"), ">="], [ui.DateTimeEdit_Data2.dateTime().toPython().strftime("%Y-%m-%d %H:%M:%S"), "<="]],
                    "p.ultima_modifica" : [[ui.DateTimeEdit_ultima_modifica.dateTime().toPython().strftime("%Y-%m-%d %H:%M:%S"), ">="], [ui.DateTimeEdit_ultima_modifica2.dateTime().toPython().strftime("%Y-%m-%d %H:%M:%S"), "<="]],
                    "p.nome" : [["" if not ui.lineEdit_Nome.text() else f"%%{ui.lineEdit_Nome.text()}%%", "LIKE"]],
                    "p.codice" : [["" if not ui.lineEdit_Codice.text() else f"%%{ui.lineEdit_Codice.text()}%%", "LIKE"]],
                    "p.cliente" : [[ui.comboBox_Cliente.currentText(), "="]] if not ui.comboBox_Cliente.currentText() == "<Qualsiasi cliente>" else [["", "="]],
                    "p.quantità_per_disegno" : [[ui.lineEdit_Quantita.text(), "="]],
                    "p.misura_di_massima" : [[ui.lineEdit_MisuraMax.text(), ">="], [ui.lineEdit_MisuraMax2.text(), "<="]],
                    "p.massa" : [[ui.lineEdit_Massa.text(), ">="], [ui.lineEdit_Massa2.text(), "<="]]
                    }
    return dizionario

def carica_documento():
    if selected := ui.tableView.selectedIndexes():
        riga_selezionata = selected[0].row()
        percorso_file = tabella[riga_selezionata][13]
    else:
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

def elimina_riga():
    if selected := ui.tableView.selectedIndexes():
        riga_selezionata = selected[0].row()
        print(f"Elimina riga {riga_selezionata}")
    else:
        print("nessuna riga selezionata")

def modifica_riga():
    global Form_modifica

    if selected := ui.tableView.selectedIndexes():
        riga_selezionata = selected[0].row()
        print(f"Modifica riga {riga_selezionata}")
        Carica_dati_iterfaccia_modifica(tabella[riga_selezionata])
        Form_modifica.show()
    else:
        print("nessuna riga selezionata")

def aggiorna_anteprima():
    if selected := ui.tableView.selectedIndexes():
        riga_selezionata = selected[0].row()
        percorso_file = tabella[riga_selezionata][13][:-5] + "png"
        try:
            immagine_anteprima = QtGui.QPixmap(percorso_file)
            ui.label_anteprima.setPixmap(immagine_anteprima)
        except:
            ui.label_anteprima.setPixmap(immagine_predefinita)
    else:
        ui.label_anteprima.setPixmap(immagine_predefinita)


########################################
######## Punto d'ingresso macro ########
########################################

immagine_predefinita = QtGui.QPixmap(cwd + "/resources/no image.png")

Form_modifica = QtWidgets.QWidget()
ui_modifica = finestra_modifica.Ui_Form()
ui_modifica.setupUi(Form_modifica)
Inizializza_iterfaccia_modifica()

# Crea la finestra
Form = QtWidgets.QWidget()
ui = interfaccia.Ui_Form()
ui.setupUi(Form)

if InizializzaIterfaccia():
    Form.show()