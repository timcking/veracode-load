import sys
import pyodbc
import logging

def insertScan(conn, scanList):
    sql = "INSERT INTO scans(analysis_id, sandbox_id, version, module_name, sandbox_name, submitter, " +\
          "generation_date, total_flaws, load_date, load_file) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

    # Insert into DB
    try:
        cursor = conn.cursor()
        cursor.execute(sql, scanList)
        conn.commit()
    except pyodbc.Error as ex:
        logging.error(str(ex))
        sys.exit(1)

def insertFlaw(conn, flawList):
    sql = "INSERT INTO flaws(analysis_id, sandbox_id, ticket_id, severity, flaw_id, remediation_status, " +\
          "cwe_id, category_name, source_file, line_num, load_date, update_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

    # Insert into DB
    try:
        cursor = conn.cursor()
        cursor.execute(sql, flawList)
    except pyodbc.Error as ex:
        logging.error(str(ex))
        sys.exit(1)

def updateFlaw(conn, flawList):
    sql = "UPDATE flaws " +\
          "   SET remediation_status = ?, " +\
          "       update_date = ? " +\
          " WHERE analysis_id = ? " +\
          "   AND sandbox_id = ? " +\
          "   AND flaw_id = ?"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, flawList)
        conn.commit()
    except pyodbc.Error as ex:
        logging.error(str(ex))
        sys.exit(1)
        
def updateFixedFlaw(conn, flawList):
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
        cursor = conn.cursor()
        cursor.execute(sql, flawList)
        conn.commit()
    except pyodbc.Error as ex:
        logging.error(str(ex))
        sys.exit(1)

def getFlawCount(conn, queryParams):
    sql = "SELECT COUNT(*) AS thecount " +\
          "  FROM flaws " +\
          " WHERE analysis_id <> ? " +\
          "   AND sandbox_id = ? " +\
          "   AND flaw_id = ? "

    try:
        cursor = conn.cursor()
        cursor.execute(sql, queryParams)
    except pyodbc.Error as ex:
        logging.error(str(ex))

    for row in cursor.fetchone():
        return int(row)
    
def getPriorFlawCount(conn, queryParams):
    sql = "SELECT COUNT(*) AS thecount " +\
          "  FROM flaws " +\
          " WHERE analysis_id <> ? " +\
          "   AND sandbox_id = ? " +\
          "   AND flaw_id = ? "

    try:
        cursor = conn.cursor()
        cursor.execute(sql, queryParams)
    except pyodbc.Error as ex:
        logging.error(str(ex))

    for row in cursor.fetchone():
        return int(row)

def getScanCount(conn, queryParams):
    sql = "SELECT COUNT(*) AS thecount " +\
          "  FROM scans " +\
          " WHERE analysis_id = ?"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, queryParams)
    except pyodbc.Error as ex:
        logging.error(str(ex))
        sys.exit(1)    

    for row in cursor.fetchone():
        return int(row)
