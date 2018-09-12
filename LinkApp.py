from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5 import QtCore
from ui_link import Ui_MainDialog

class MainDialog(QDialog):
    def __init__(self, *positional_parameters, **keyword_parameters):
        super(MainDialog, self).__init__()

        # Set up the user interface from Designer.
        self.ui = Ui_MainDialog()
        self.resize(550, 350)
        self.setMinimumSize(QtCore.QSize(450, 350))
        self.ui.setupUi(self)

        # self.ui.buttonBox.clicked.connect(self.close)

        # self.ui.listSenate.clicked.connect(self.onSenateClick)
        # self.ui.listHouse.clicked.connect(self.onHouseClick)
        
if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    # dialog = MainDialog(optional="Casablanca")
    dialog = MainDialog()
    sys.exit(dialog.exec_())
