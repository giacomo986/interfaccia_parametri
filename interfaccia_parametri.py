import sys, os
from PyQt5 import QtWidgets, QtCore, QtGui
import resources.interfaccia as interfaccia
import csv, datetime
from resources.CsvTableModelClass import CsvTableModel

def InizializzaDati():
    modelClienti = CsvTableModel(cwd + "/resources/clienti.csv")
    for element in range(0, modelClienti.NumbersOfRows()):
        ui.comboBox_Cliente.addItem(modelClienti.getCell(element, 0), modelClienti.getCell(element, 1))
    
    modelMateriali = CsvTableModel(cwd + "/resources/materiali.csv")
    for element in range(0, modelMateriali.NumbersOfRows()):
        ui.comboBox_Materiale.addItem(modelMateriali.getCell(element, 0), modelMateriali.getCell(element, 1))

    ui.CancelButton.clicked.connect(ChiudiApplicazione)
    ui.AcceptButton.clicked.connect(SalvaDati)

def SalvaDati():
    if ui.lineEdit_Riferimento.text() == "":
        qm = QtWidgets.QMessageBox
        question = qm.information(None, 'Campo "Riferimento" vuoto', 'Il campo "Riferimento" è vuoto, riempire il campo "Riferimento" prima di confermare')
        return

    nomeFile = str(cwd + "/" + ui.lineEdit_Riferimento.text() + ".csv")
    if not os.path.exists(nomeFile):
        open(nomeFile, "w")
    else:
        qm = QtWidgets.QMessageBox
        question = qm.question(None, "File già esistente", "File già esistente. Vuoi sovrascrivere il file?", qm.Yes | qm.No)
        if (question == qm.No):
            qm.information(None, "Informazione", "Nessuna modifica")
            return

    with open(nomeFile, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=",",
                                quotechar="|", quoting=csv.QUOTE_MINIMAL)
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
                        [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")] +
                        [ui.lineEdit_Nome.text()] +
                        [ui.lineEdit_Codice.text()] +
                        [ui.comboBox_Cliente.currentText()] +
                        [ui.lineEdit_Quantita.text()] +
                        [ui.lineEdit_MisuraMax.text()] +
                        [ui.lineEdit_Massa.text()])

    qm = QtWidgets.QMessageBox
    qm.information(None, "Informazione", "File salvato.")

def ChiudiApplicazione():
    Form.close()
    #QtCore.QCoreApplication.instance().quit()

if __name__ == "__main__":
    cwd = os.getcwd()
    #app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = interfaccia.Ui_Form()
    ui.setupUi(Form)
    InizializzaDati()
    Form.show()
    sys.exit(app.exec_())