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

def aggiorna_Testo():
    global text, text2
    text = text + non_block_read(sub_proc.stdout)

    if (text2 == text):
        return
    text2 = text
    window.textEdit.setText(text2)

    if sub_proc.poll() != None: # si .poll() == None Popen non ha finito
        timer.stop()
        return

def avvia_timer():
    timer.timeout.connect(aggiorna_Testo)
    timer.start(100)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    ui_file = QtCore.QFile("console_in_qt.ui")
    ui_file.open(QtCore.QFile.ReadOnly)

    loader = QtUiTools.QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()
    window.show()
    timer = QtCore.QTimer()
    text, text2 = "", ""
    window.pushButton.clicked.connect(avvia_timer)
    window.textEdit.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)

    sys.exit(app.exec_())
