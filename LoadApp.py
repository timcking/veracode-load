import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from ui_veracode import Ui_MainWindow
import VcParse

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.setMinimumSize(QSize(700, 200))
        self.ui.setupUi(self)

        self.ui.buttonLoad.clicked.connect(self.onLoadClick)
        self.ui.buttonClose.clicked.connect(self.onCloseClick)

        self.ui.buttonLoad.setEnabled(False)
        self.ui.textFile.textChanged.connect(self.toggleButton)

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile = self.ui.actionOpen
        openFile.triggered.connect(self.showDialog)

        menubar = self.ui.menuBar
        menuFile = self.ui.menuFile
        menuFile.addAction(openFile)     

        self.show()

    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'xml/')

        if fname[0]:
            self.ui.textFile.setText(fname[0])
            self.ui.statusBar.showMessage('Ready')
        else:
            self.ui.statusBar.showMessage('File not found!')

    def onLoadClick(self):
        xmlFile = self.ui.textFile.text()
        total_scans, analysis_id, sandbox_id = VcParse.getScans(xmlFile)
        
        if total_scans == -1 :
            self.ui.statusBar.showMessage("Analysis ID %s already exists, ignoring this scan" % (analysis_id))
            return
        
        total_flaws = VcParse.getFlaws(xmlFile, analysis_id, sandbox_id)

        if total_scans == total_flaws:
            self.ui.statusBar.showMessage('Completed, Total Flaws = ' + str(total_flaws))
        else:
            self.ui.statusBar.showMessage('Flaw count does not match! ' + str(total_scans) +
            ' vs. ' + str(total_flaws))
            
    def toggleButton(self):
        if len(self.ui.textFile.text()) > 0:
            self.ui.buttonLoad.setEnabled(True)
        else:
            self.ui.buttonLoad.setEnabled(False)

    def onCloseClick(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = AppWindow()
    w.show()

    # Vs Code bug
    # sys.exit(app.exec_())
    app.exec_()
