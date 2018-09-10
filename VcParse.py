import xml.etree.ElementTree as ET
import sys
import pyodbc
from datetime import datetime
import logging

# Every object in the tree has this at the beginning
URL = "{https://www.veracode.com/schema/reports/export/1.0}"

CONN_STR = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=.\\data\VeracodeAug.accdb;'
)

load_date = datetime.now()

def getScans(xml_file):
    logName = xml_file.replace(".xml", ".log").replace("xml/", "log/")
    logging.basicConfig(filename=logName, format='%(levelname)s: %(message)s', filemode='w', level=logging.DEBUG)
    
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Need to get analysis_id first
    for dr in root.iter(URL + "detailedreport"):
        analysis_id = int(dr.attrib["analysis_id"])
        sandbox_id = int(dr.attrib["sandbox_id"])
        total_scans = int((dr.attrib["total_flaws"]))
        sandbox_name = dr.attrib["sandbox_name"]
        submitter = dr.attrib["submitter"]
        str_gen_date = dr.attrib["generation_date"]

        generation_date = datetime.strptime(str_gen_date, '%Y-%m-%d %H:%M:%S %Z')

    for sa in root.findall("./" + URL + "static-analysis"):
        version = sa.attrib["version"]

    strNode = "./" + URL + "static-analysis/" + URL + "modules/" + URL + "module"
    for flaw in root.findall(strNode):
        module_name = flaw.attrib["name"]

    # Check for existing
    queryParams = [analysis_id, sandbox_id]
    scanCount = getScanCount(queryParams)
            
    if scanCount > 0:
        logging.info("IGNORING existing scan for analysis_id %s, sandbox_id %s " % (str(analysis_id), str(sandbox_id)))
    else:
        # Write scans
        scanList = [int(analysis_id), int(sandbox_id), version, module_name, sandbox_name, submitter,
                    generation_date, int(total_scans), load_date, xml_file.replace("xml/", "")]

        insertScan(scanList)

    logging.info("Scan count: %s" % total_scans)
    return total_scans, analysis_id, sandbox_id

def getFlaws(xml_file, analysis_id, sandbox_id):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    conn = pyodbc.connect(CONN_STR)

    # Write flaws
    row = 1
    strNode = "./" + URL + "severity/" + URL + "category/" + URL + "cwe/" + URL + "staticflaws/" + URL + "flaw"
    for cwe in root.findall(strNode):
        remediation_status = (cwe.attrib["remediation_status"])

        # Ignore those with fixed status
        if remediation_status != "Fixed":
            severity = (cwe.attrib["severity"])
            issueid = (cwe.attrib["issueid"])
            cweid = (cwe.attrib["cweid"])
            categoryname = (cwe.attrib["categoryname"])
            source_file = (cwe.attrib["sourcefile"])
            line_num = (cwe.attrib["line"])

            # Placeholder for linking with tickets
            ticket_id = None

            # Check for existing
            queryParams = [analysis_id, sandbox_id, issueid]
            flawCount = getFlawCount(conn, queryParams)

            if (flawCount > 0):
                logging.info("UPDATING existing flaw for analysis_id: %s, sandbox_id: %s, issue_id: %s"
                       % (str(analysis_id), str(sandbox_id), str(issueid)))
                
                flawList = [remediation_status, load_date, int(analysis_id), int(sandbox_id), int(issueid)]
                updateFlaw(conn, flawList)
            else:
                update_date = None
                flawList = [int(analysis_id), int(sandbox_id), ticket_id, int(severity), int(issueid), remediation_status,
                            int(cweid), categoryname, source_file, int(line_num), load_date, update_date]
                insertFlaw(conn, flawList)

            row += 1

    conn.commit()
    conn.close()

    total_flaws = (row - 1)
    logging.info ("Flaw count: %s" % total_flaws)
    
    return total_flaws

def insertScan(scanList):
    sql = "INSERT INTO scans(analysis_id, sandbox_id, version, module_name, sandbox_name, submitter, " +\
          "generation_date, total_flaws, load_date, load_file) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

    # Insert into DB
    try:
        conn = pyodbc.connect(CONN_STR)
        cursor = conn.cursor()
        cursor.execute(sql, scanList)
        conn.commit()
        conn.close()
    except pyodbc.Error as ex:
        logging.error(ex)
        sys.exit(1)

def insertFlaw(conn, flawList):
    sql = "INSERT INTO flaws(analysis_id, sandbox_id, ticket_id, severity, issue_id, remediation_status, " +\
          "cwe_id, category_name, source_file, line_num, load_date, update_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

    # Insert into DB
    try:
        cursor = conn.cursor()
        cursor.execute(sql, flawList)
    except pyodbc.Error as ex:
        logging.error(ex)
        sys.exit(1)

def updateFlaw(conn, flawList):
    sql = "UPDATE flaws " +\
          "   SET remediation_status = ?, " +\
          "       update_date = ? " +\
          " WHERE analysis_id = ? " +\
          "   AND sandbox_id = ? " +\
          "   AND issue_id = ?"

    try:
        cursor = conn.cursor()
        cursor.execute(sql, flawList)
    except pyodbc.Error as ex:
        logging.error(ex)
        sys.exit(1)

def getFlawCount(conn, queryParams):

    sql = "SELECT COUNT(*) AS thecount " +\
          "  FROM flaws " +\
          " WHERE analysis_id = ? " +\
          "   AND sandbox_id = ? " +\
          "   AND issue_id = ? "

    try:
        cursor = conn.cursor()
        cursor.execute(sql, queryParams)
    except pyodbc.Error as ex:
        logging.error(ex)

    for row in cursor.fetchone():
        return int(row)

def getScanCount(queryParams):
    sql = "SELECT COUNT(*) AS thecount " +\
          "  FROM scans " +\
          " WHERE analysis_id = ? " +\
          "   AND sandbox_id = ?"
    try:
        conn = pyodbc.connect(CONN_STR)
        cursor = conn.cursor()
        cursor.execute(sql, queryParams)
    except pyodbc.Error as ex:
        logging.error(ex)
        sys.exit(1)    

    for row in cursor.fetchone():
        conn.close()
        return int(row)

def main(xml_file):
    total_scans, analysis_id, sandbox_id = getScans(xml_file)
    total_flaws = getFlaws(xml_file, analysis_id, sandbox_id)

    if total_scans != total_flaws:
        logging.error("Flaw counts do not match!")
        sys.exit(1)
    print("End")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print ("Usage: " + sys.argv[0] + " xml_file")
        sys.exit(1)
        
    xml_file = sys.argv[1]
    main(xml_file)
