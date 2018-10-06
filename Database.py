import sys
import pyodbc
import logging

class Database:
    def __init__(self):
        CONN_STR = (
           r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
           r'DBQ=.\\data\\Veracode.accdb;'
        )
        
        self.conn = pyodbc.connect(CONN_STR)

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def insertScan(self, scanList):
        sql = "INSERT INTO scans(analysis_id, sandbox_id, version, module_name, sandbox_name, submitter, " +\
            "generation_date, total_flaws, load_date, load_file) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

        # Insert into DB
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, scanList)
        except pyodbc.Error as ex:
            logging.error(str(ex))
            sys.exit(1)

    def insertFlaw(self, flawList):
        sql = "INSERT INTO flaws(analysis_id, sandbox_id, ticket_id, severity, flaw_id, remediation_status, " +\
            "cwe_id, category_name, source_file, line_num, load_date, update_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

        # Insert into DB
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, flawList)
        except pyodbc.Error as ex:
            logging.error(str(ex))
            sys.exit(1)

    def updateFlaw(self, flawList):
        sql = "UPDATE flaws " +\
            "   SET remediation_status = ?, " +\
            "       update_date = ? " +\
            " WHERE analysis_id = ? " +\
            "   AND sandbox_id = ? " +\
            "   AND flaw_id = ?"
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, flawList)
        except pyodbc.Error as ex:
            logging.error(str(ex))
            sys.exit(1)
            
    def updateFixedFlaw(self, flawList):
        # TCK ToDo, test
        # Update status for other analysis_id's for the same sandbox/flaw
        sql = "UPDATE flaws " +\
            "   SET remediation_status = 'Fixed', " +\
            "       update_date = ? " +\
            " WHERE analysis_id <> ? " +\
            "   AND sandbox_id = ? " +\
            "   AND flaw_id = ?"
        
        # Delete flaws for other analysis_id's for the same sandbox/flaw
        #sql = "DELETE FROM flaws " +\
        #      " WHERE analysis_id <> ? " +\
        #      "   AND sandbox_id = ? " +\
        #      "   AND flaw_id = ?"
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, flawList)
        except pyodbc.Error as ex:
            logging.error(str(ex))
            sys.exit(1)

    def getFlawCount(self, queryParams):
        sql = "SELECT COUNT(*) AS thecount " +\
            "  FROM flaws " +\
            " WHERE analysis_id <> ? " +\
            "   AND sandbox_id = ? " +\
            "   AND flaw_id = ? "

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, queryParams)
        except pyodbc.Error as ex:
            logging.error(str(ex))

        for row in cursor.fetchone():
            return int(row)
        
    def getPriorFlawCount(self, queryParams):
        sql = "SELECT COUNT(*) AS thecount " +\
            "  FROM flaws " +\
            " WHERE analysis_id <> ? " +\
            "   AND sandbox_id = ? " +\
            "   AND flaw_id = ? "

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, queryParams)
        except pyodbc.Error as ex:
            logging.error(str(ex))

        for row in cursor.fetchone():
            return int(row)

    def getScanCount(self, queryParams):
        sql = "SELECT COUNT(*) AS thecount " +\
            "  FROM scans " +\
            " WHERE analysis_id = ?"
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, queryParams)
        except pyodbc.Error as ex:
            logging.error(str(ex))
            sys.exit(1)    

        for row in cursor.fetchone():
            return int(row)
