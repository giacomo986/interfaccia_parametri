from PySide2 import QtCore, QtGui, QtWidgets
from Equation import Expression

class LineEdit_Expr(QtWidgets.QLineEdit):
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return:
            #print("Premuto tasto invio")
            self.risolvi_espressione()
        QtWidgets.QLineEdit.keyPressEvent(self, event)

    def focusOutEvent(self, event):
        #print('focus out event')
        self.risolvi_espressione()
        QtWidgets.QLineEdit.focusOutEvent(self, event)
    
    def risolvi_espressione(self):
        if self.text():
            try:
                espressione = Expression(self.text())
                self.setText(str(espressione()))
            except:
                print("errore nella risoluzione della espressione. Assicurarsi che sia scritta in modo corretto senza caratteri estranei.")
                self.setText("")

class Ui_Form(object):
    def setupUi(self, Form):
        
        Form.resize(1000, 600)

        reg_ex = QtCore.QRegExp(r"^([-+/*]?\d+(\.\d+)?)*") # Regular Expression per filtrare solo valori numerici dove necessario

        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.horizontalLayout2 = QtWidgets.QHBoxLayout()

        self.tableView = QtWidgets.QTableView(Form)
        self.tableView.setSortingEnabled(True)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.horizontalLayout2.addWidget(self.tableView)

        self.label_anteprima = QtWidgets.QLabel(Form)
        self.horizontalLayout2.addWidget(self.label_anteprima)

        #pixmap = QtGui.QPixmap("resources/no image.png")
        self.label_anteprima.setFixedSize(200, 200)
        self.label_anteprima.setScaledContents(True)
        #self.label_anteprima.setPixmap(pixmap)  

        self.verticalLayout.addLayout(self.horizontalLayout2)
        self.gridLayout = QtWidgets.QGridLayout()

        self.label_4 = QtWidgets.QLabel(Form)
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)

        self.label_12 = QtWidgets.QLabel(Form)
        self.gridLayout.addWidget(self.label_12, 12, 0, 1, 1)

        self.label_7 = QtWidgets.QLabel(Form)
        self.gridLayout.addWidget(self.label_7, 7, 0, 1, 1)

        self.label = QtWidgets.QLabel(Form)
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lineEdit_Riferimento = QtWidgets.QLineEdit(Form)
        self.gridLayout.addWidget(self.lineEdit_Riferimento, 0, 6, 1, 1)

        self.label_2 = QtWidgets.QLabel(Form)
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.lineEdit_CodicePadre = QtWidgets.QLineEdit(Form)
        self.gridLayout.addWidget(self.lineEdit_CodicePadre, 1, 6, 1, 1)

        self.label_5 = QtWidgets.QLabel(Form)
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)

        self.label_3 = QtWidgets.QLabel(Form)
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.lineEdit_Macchina = QtWidgets.QLineEdit(Form)
        self.gridLayout.addWidget(self.lineEdit_Macchina, 2, 6, 1, 1)

        self.comboBox_Denominazione = QtWidgets.QComboBox(Form)
        self.gridLayout.addWidget(self.comboBox_Denominazione, 4, 6, 1, 1)

        self.lineEdit_Massa = LineEdit_Expr(Form)
        Massa_input_validator = QtGui.QRegExpValidator(reg_ex, self.lineEdit_Massa)
        self.lineEdit_Massa.setValidator(Massa_input_validator)
        self.gridLayout.addWidget(self.lineEdit_Massa, 12, 6, 1, 1)

        self.lineEdit_Massa2 = LineEdit_Expr(Form)
        Massa2_input_validator = QtGui.QRegExpValidator(reg_ex, self.lineEdit_Massa2)
        self.lineEdit_Massa2.setValidator(Massa2_input_validator)
        self.gridLayout.addWidget(self.lineEdit_Massa2, 12, 7, 1, 1)
        
        self.lineEdit_Quantita = LineEdit_Expr(Form)
        Quantita_input_validator = QtGui.QRegExpValidator(reg_ex, self.lineEdit_Quantita)
        self.lineEdit_Quantita.setValidator(Quantita_input_validator)
        self.gridLayout.addWidget(self.lineEdit_Quantita, 10, 6, 1, 1)

        self.lineEdit_Codice = QtWidgets.QLineEdit(Form)
        self.gridLayout.addWidget(self.lineEdit_Codice, 8, 6, 1, 1)

        self.lineEdit_MisuraMax = LineEdit_Expr(Form)
        MisuraMax_input_validator = QtGui.QRegExpValidator(reg_ex, self.lineEdit_MisuraMax)
        self.lineEdit_MisuraMax.setValidator(MisuraMax_input_validator)
        self.gridLayout.addWidget(self.lineEdit_MisuraMax, 11, 6, 1, 1)

        self.lineEdit_MisuraMax2 = LineEdit_Expr(Form)
        MisuraMax2_input_validator = QtGui.QRegExpValidator(reg_ex, self.lineEdit_MisuraMax2)
        self.lineEdit_MisuraMax2.setValidator(MisuraMax2_input_validator)
        self.gridLayout.addWidget(self.lineEdit_MisuraMax2, 11, 7, 1, 1)

        self.comboBox_Cliente = QtWidgets.QComboBox(Form)
        self.gridLayout.addWidget(self.comboBox_Cliente, 9, 6, 1, 1)

        self.comboBox_Materiale = QtWidgets.QComboBox(Form)
        self.gridLayout.addWidget(self.comboBox_Materiale, 3, 6, 1, 1)

        self.label_8 = QtWidgets.QLabel(Form)
        self.gridLayout.addWidget(self.label_8, 8, 0, 1, 1)

        self.label_9 = QtWidgets.QLabel(Form)
        self.gridLayout.addWidget(self.label_9, 9, 0, 1, 1)

        self.lineEdit_Nome = QtWidgets.QLineEdit(Form)
        self.gridLayout.addWidget(self.lineEdit_Nome, 7, 6, 1, 1)

        self.label_6 = QtWidgets.QLabel(Form)
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)

        self.label_6_1 = QtWidgets.QLabel(Form)
        self.gridLayout.addWidget(self.label_6_1, 6, 0, 1, 1)

        self.label_10 = QtWidgets.QLabel(Form)
        self.gridLayout.addWidget(self.label_10, 10, 0, 1, 1)

        self.label_11 = QtWidgets.QLabel(Form)
        self.gridLayout.addWidget(self.label_11, 11, 0, 1, 1)

        self.DateTimeEdit_Data = QtWidgets.QDateTimeEdit(Form)
        self.gridLayout.addWidget(self.DateTimeEdit_Data, 5, 6, 1, 1)

        self.DateTimeEdit_Data2 = QtWidgets.QDateTimeEdit(Form)
        self.gridLayout.addWidget(self.DateTimeEdit_Data2, 5, 7, 1, 1)

        self.DateTimeEdit_ultima_modifica = QtWidgets.QDateTimeEdit(Form)
        self.gridLayout.addWidget(self.DateTimeEdit_ultima_modifica, 6, 6, 1, 1)

        self.DateTimeEdit_ultima_modifica2 = QtWidgets.QDateTimeEdit(Form)
        self.gridLayout.addWidget(self.DateTimeEdit_ultima_modifica2, 6, 7, 1, 1)
    
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)

        self.horizontalSpacer = QtWidgets.QSpacerItem(200, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.CancelButton = QtWidgets.QPushButton(Form)
        self.horizontalLayout.addWidget(self.CancelButton)

        self.ModifyButton = QtWidgets.QPushButton(Form)
        self.horizontalLayout.addWidget(self.ModifyButton)

        self.DeleteButton = QtWidgets.QPushButton(Form)
        self.horizontalLayout.addWidget(self.DeleteButton)

        self.SearchButton = QtWidgets.QPushButton(Form)
        self.horizontalLayout.addWidget(self.SearchButton)

        self.AcceptButton = QtWidgets.QPushButton(Form)
        self.horizontalLayout.addWidget(self.AcceptButton)

        self.verticalLayout.addLayout(self.gridLayout)
        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Carica Pezzo"))
        self.label_4.setText(_translate("Form", "Materiale:"))
        self.label_12.setText(_translate("Form", "Massa (grammi) (da ... a ...):"))
        self.label_7.setText(_translate("Form", "Nome:"))
        self.label.setText(_translate("Form", "Riferimento:"))
        self.lineEdit_Riferimento.setToolTip(_translate("Form", "Codice disegno (testo libero)"))
        self.label_2.setText(_translate("Form", "Codice padre:"))
        self.lineEdit_CodicePadre.setToolTip(_translate("Form", "testo, assieme fittizio"))
        self.label_5.setText(_translate("Form", "Denominazione profilo:"))
        self.label_3.setText(_translate("Form", "Macchina:"))
        self.lineEdit_Macchina.setToolTip(_translate("Form", "testo libero, facoltativo"))
        self.comboBox_Denominazione.setToolTip(_translate("Form", "menu a tendina con nomi standard"))
        self.lineEdit_Massa.setToolTip(_translate("Form", "automatica, volume per densità (collegata a materiale)"))
        self.lineEdit_Quantita.setToolTip(_translate("Form", "valore numerico, default 1, editabile"))
        self.lineEdit_Codice.setToolTip(_translate("Form", "ridondante (facoltativo)"))
        self.lineEdit_MisuraMax.setToolTip(_translate("Form", "automatiche, vedi box ingombro (orientamento sempre uguale)"))
        self.comboBox_Cliente.setToolTip(_translate("Form", "associare a tabella esterna editabile"))
        self.comboBox_Materiale.setToolTip(_translate("Form", "FERRO, INOX (legato a densità) associare a tabella esterna editabile"))
        self.label_8.setText(_translate("Form", "Codice:"))
        self.label_9.setText(_translate("Form", "Cliente:"))
        self.lineEdit_Nome.setToolTip(_translate("Form", "ridondante, nome del cliente (facoltativo)"))
        self.label_6.setText(_translate("Form", "Data di creazione (da ... a ...):"))
        self.label_6_1.setText(_translate("Form", "Data ultima modifica (da ... a ...):"))
        self.label_10.setText(_translate("Form", "Q.tà per Disegno:"))
        self.label_11.setText(_translate("Form", "Misura di massima (da ... a ...):"))
        self.CancelButton.setText(_translate("Form", "Chiudi"))
        self.SearchButton.setText(_translate("Form", "Cerca"))
        self.AcceptButton.setText(_translate("Form", "Carica"))
        self.ModifyButton.setText(_translate("Form", "Modifica riga"))
        self.DeleteButton.setText(_translate("Form", "Elimina riga"))

