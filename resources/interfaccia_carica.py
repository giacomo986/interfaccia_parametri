# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interfaccia_carica.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(566, 500)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)

        self.tableView = QtWidgets.QTableView(Form)

        self.verticalLayout.addWidget(self.tableView)
        self.gridLayout = QtWidgets.QGridLayout()

        self.label = QtWidgets.QLabel(Form)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit_Quantita = QtWidgets.QLineEdit(Form)

        self.gridLayout.addWidget(self.lineEdit_Quantita, 9, 1, 1, 1)
        self.comboBox_Materiale = QtWidgets.QComboBox(Form)

        self.gridLayout.addWidget(self.comboBox_Materiale, 3, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(Form)

        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(Form)

        self.gridLayout.addWidget(self.label_12, 11, 0, 1, 1)
        self.lineEdit_Macchina = QtWidgets.QLineEdit(Form)

        self.gridLayout.addWidget(self.lineEdit_Macchina, 2, 1, 1, 1)
        self.lineEdit_CodicePadre = QtWidgets.QLineEdit(Form)

        self.gridLayout.addWidget(self.lineEdit_CodicePadre, 1, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(Form)

        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(Form)

        self.gridLayout.addWidget(self.label_8, 7, 0, 1, 1)
        self.lineEdit_Riferimento = QtWidgets.QLineEdit(Form)

        self.gridLayout.addWidget(self.lineEdit_Riferimento, 0, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(Form)

        self.gridLayout.addWidget(self.label_7, 6, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(Form)

        self.gridLayout.addWidget(self.label_10, 9, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Form)

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(Form)

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.lineEdit_Nome = QtWidgets.QLineEdit(Form)

        self.gridLayout.addWidget(self.lineEdit_Nome, 6, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(Form)

        self.gridLayout.addWidget(self.label_9, 8, 0, 1, 1)
        self.lineEdit_Codice = QtWidgets.QLineEdit(Form)

        self.gridLayout.addWidget(self.lineEdit_Codice, 7, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(Form)

        self.gridLayout.addWidget(self.label_11, 10, 0, 1, 1)
        self.lineEdit_MisuraMax = QtWidgets.QLineEdit(Form)

        self.gridLayout.addWidget(self.lineEdit_MisuraMax, 10, 1, 1, 1)
        self.comboBox_Denominazione = QtWidgets.QComboBox(Form)

        self.gridLayout.addWidget(self.comboBox_Denominazione, 4, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(Form)

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.lineEdit_Data = QtWidgets.QLineEdit(Form)

        self.gridLayout.addWidget(self.lineEdit_Data, 5, 1, 1, 1)
        self.lineEdit_Massa = QtWidgets.QLineEdit(Form)

        self.gridLayout.addWidget(self.lineEdit_Massa, 11, 1, 1, 1)
        self.comboBox_Cliente = QtWidgets.QComboBox(Form)

        self.gridLayout.addWidget(self.comboBox_Cliente, 8, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)

        self.CancelButton = QtWidgets.QPushButton(Form)

        self.horizontalLayout.addWidget(self.CancelButton)
        self.AcceptButton = QtWidgets.QPushButton(Form)

        self.horizontalLayout.addWidget(self.AcceptButton)
        self.gridLayout.addLayout(self.horizontalLayout, 12, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Salva Informazioni"))
        self.label.setText(_translate("Form", "Riferimento:"))
        self.lineEdit_Quantita.setToolTip(_translate("Form", "valore numerico, default 1, editabile"))
        self.lineEdit_Quantita.setText(_translate("Form", "1"))
        self.comboBox_Materiale.setToolTip(_translate("Form", "FERRO, INOX (legato a densità) associare a tabella esterna editabile"))
        self.label_5.setText(_translate("Form", "Denominazione profilo:"))
        self.label_12.setText(_translate("Form", "Massa:"))
        self.lineEdit_Macchina.setToolTip(_translate("Form", "testo libero, facoltativo"))
        self.lineEdit_CodicePadre.setToolTip(_translate("Form", "testo, assieme fittizio"))
        self.label_6.setText(_translate("Form", "Data di creazione:"))
        self.label_8.setText(_translate("Form", "Codice:"))
        self.lineEdit_Riferimento.setToolTip(_translate("Form", "Codice disegno (testo libero)"))
        self.label_7.setText(_translate("Form", "Nome:"))
        self.label_10.setText(_translate("Form", "Q.tà per Disegno:"))
        self.label_2.setText(_translate("Form", "Codice padre:"))
        self.label_3.setText(_translate("Form", "Macchina:"))
        self.lineEdit_Nome.setToolTip(_translate("Form", "ridondante, nome del cliente (facoltativo)"))
        self.label_9.setText(_translate("Form", "Cliente:"))
        self.lineEdit_Codice.setToolTip(_translate("Form", "ridondante (facoltativo)"))
        self.label_11.setText(_translate("Form", "Misura di massima:"))
        self.lineEdit_MisuraMax.setToolTip(_translate("Form", "automatiche, vedi box ingombro (orientamento sempre uguale)"))
        self.comboBox_Denominazione.setToolTip(_translate("Form", "menu a tendina con nomi standard"))
        self.label_4.setText(_translate("Form", "Materiale:"))
        self.lineEdit_Massa.setToolTip(_translate("Form", "automatica, volume per densità (collegata a materiale)"))
        self.comboBox_Cliente.setToolTip(_translate("Form", "associare a tabella esterna editabile"))
        self.CancelButton.setText(_translate("Form", "Annulla"))
        self.AcceptButton.setText(_translate("Form", "Conferma"))
