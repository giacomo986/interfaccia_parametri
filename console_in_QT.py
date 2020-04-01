import subprocess, sys
from PySide2 import QtWidgets, QtCore, QtGui, QtUiTools

def Testo():
    #window.textEdit.setText("aaaaaaaaaaaaaa")
    window.textEdit.append(subprocess.check_output(['pip', 'install', "mysql-connector-python"]))
    pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    ui_file = QtCore.QFile("console_in_qt.ui")
    ui_file.open(QtCore.QFile.ReadOnly)

    loader = QtUiTools.QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()
    window.show()
    window.pushButton.clicked.connect(Testo)

    sys.exit(app.exec_())
