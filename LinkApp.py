from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from PyQt5 import QtCore
from ui_link import Ui_MainDialog
import pyodbc

CONN_STR = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=.\\data\\Veracode.accdb;'
)

conn = pyodbc.connect(CONN_STR)

class MainDialog(QDialog):
    def __init__(self, *positional_parameters, **keyword_parameters):
        super(MainDialog, self).__init__()

        # Set up the user interface from Designer.
        self.ui = Ui_MainDialog()
        self.resize(550, 350)
        self.setMinimumSize(QtCore.QSize(450, 350))
        self.ui.setupUi(self)

        # Connect buttons
        self.ui.buttonClose.clicked.connect(self.close)
        self.ui.buttonLink.clicked.connect(self.onLinkClick)
        
    def onLinkClick(self):
        if self.ui.textAnalysisId.text():
            analysisID = self.ui.textAnalysisId.text()
        else:
            QMessageBox.about(self, "Error", "Analysis ID required")
            self.ui.textAnalysisId.setFocus()
            return
        
        if self.ui.textSandboxId.text():
            sandboxID = self.ui.textSandboxId.text()
        else:
            QMessageBox.about(self, "Error", "Sandbox ID required")
            self.ui.textSandboxId.setFocus()
            return

        if self.ui.textTicketId.text():
            ticketID = self.ui.textTicketId.text()
        else:
            QMessageBox.about(self, "Error", "Ticket ID required")
            self.ui.textTicketId.setFocus()
            return
        
        if self.ui.textFlaw.toPlainText():
            strFlaws = self.ui.textFlaw.toPlainText().replace("\n", ",")
        else:
            QMessageBox.about(self, "Error", "One or more flaws required")
            self.ui.textFlaw.setFocus()
            return
        
        # Check if flaw list starts with an alpha, maybe garbage pasted in
        if strFlaws[0].isalpha():
            QMessageBox.about(self, "Error",  "Check for text in flaw list")
            return
        
        # Get rid of last comma
        if strFlaws.endswith(","):
            strFlaws = strFlaws[:-1]
            
        queryParams = [ticketID, sandboxID, analysisID, strFlaws]
        count = self.updateLinkFlaws(queryParams)
        QMessageBox.about(self, "Ticket ID " + ticketID, str(count) + " flaws updated")
    
    def updateLinkFlaws(self, queryParams):
        sql =  "UPDATE flaws " +\
               "  SET ticket_id = " + queryParams[0] + " " +\
               "WHERE sandbox_id =  " + queryParams[1] +\
               "  AND analysis_id = " + queryParams[2] +\
               "  AND flaw_id IN (" + queryParams[3] + ")"
        try:
            cursor = conn.cursor()
            row_count = cursor.execute(sql).rowcount
            conn.commit()
        except pyodbc.Error as ex:
            QMessageBox.about(self, "Error", str(ex))
            row_count = 0
            
        return row_count
    
    # TCK ToDo
    def updateFlawsParam(self, queryParams):
        print (len(queryParams[2]))
        placeholders = ",".join("?" * len(queryParams[2]))
        sql =  "UPDATE flaws " +\
               "   SET ticket_id = ? " +\
               "WHERE sandbox_id = ? " +\
               "  AND flaw_id IN (%s)" % placeholders
        try:
            cursor = conn.cursor()
            row_count = cursor.execute(sql, queryParams).rowcount
            conn.commit()
        except pyodbc.Error as ex:
            QMessageBox.about(self, "Error", str(ex))
            row_count = 0
            
        return row_count    

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    dialog = MainDialog()
    # Vs Code bug
    # sys.exit(dialog.exec_())
    dialog.exec_()
    conn.close()