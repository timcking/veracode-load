from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from PyQt5 import QtCore
from ui_link import Ui_MainDialog
import pyodbc

CONN_STR = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=.\\data\\Veracode.accdb;'
)

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
            
        queryParams = [ticketID, sandboxID, strFlaws]
        count = self.updateFlaws(queryParams)
        QMessageBox.about(self, "Ticket ID " + ticketID, str(count) + " flaws updated")
        
    def updateFlaws(self, queryParams):
        sql =  "UPDATE flaws " +\
               "  SET ticket_id = " + queryParams[0] + " " +\
               "WHERE sandbox_id =  " + queryParams[1]+\
               "  AND flaw_id IN (" + queryParams[2] + ")"
        try:
            conn = pyodbc.connect(CONN_STR)
            cursor = conn.cursor()
            row_count = cursor.execute(sql).rowcount
            conn.commit()
            conn.close()
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
            conn = pyodbc.connect(CONN_STR)
            cursor = conn.cursor()
            row_count = cursor.execute(sql, queryParams).rowcount
            conn.commit()
            conn.close()
        except pyodbc.Error as ex:
            QMessageBox.about(self, "Error", str(ex))
            row_count = 0
            
        return row_count    
            
    def getScanCount(self):
        sql = """
              SELECT COUNT(*) AS thecount
                FROM scans
              """
        try:
            conn = pyodbc.connect(CONN_STR)
            cursor = conn.cursor()
            cursor.execute(sql)
        except pyodbc.Error as ex:
            # logging.error(ex)
            sys.exit(1)    

        for row in cursor.fetchone():
            conn.close()
            return int(row)

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    dialog = MainDialog()
    # Vs Code bug
    # sys.exit(dialog.exec_())
    dialog.exec_()
