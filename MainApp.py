import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from ui_veracode import Ui_MainWindow

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile = self.ui.actionOpen
        openFile.triggered.connect(self.showDialog)

        menubar = self.ui.menuBar
        menuFile = self.ui.menuFile
        menuFile.addAction(openFile)     

        self.show()

    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '.')

        if fname[0]:
            f = open(fname[0], 'r')

            with f:
                data = f.read()
                self.ui.textFile.setText(data)

if __name__ == '__main__':
   app = QApplication(sys.argv)
   w = AppWindow()
   w.show()
   sys.exit(app.exec_())
