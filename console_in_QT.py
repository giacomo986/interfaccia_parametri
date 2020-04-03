import subprocess, sys, os, fcntl
from PySide2 import QtWidgets, QtCore, QtGui, QtUiTools
from subprocess import Popen, PIPE

sub_proc = Popen("ping -c 10 localhost", stdout=PIPE, shell=True)
sub_outp = ""

def non_block_read(output):
    ''' even in a thread, a normal read with block until the buffer is full '''
    fd = output.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
    try:
        return output.read().decode("utf-8")
    except:
        return ''

def Testo():
    window.textEdit.append(non_block_read(sub_proc.stdout))
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
