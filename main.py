import sys
from PyQt5 import QtWidgets
import interfaccia

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = interfaccia.Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())