import xml.etree.ElementTree as ET
import sys
import pyodbc
from datetime import datetime

# Every object in the tree has this at the beginning
URL = "{https://www.veracode.com/schema/reports/export/1.0}"

CONN_STR = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=.\\data\VeracodeAug.accdb;'
)

LOAD_ERR = None

load_date = datetime.now()

def getScans(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Need to get analysis_id first
    for dr in root.iter(URL + "detailedreport"):
        analysis_id = int(dr.attrib["analysis_id"])
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

    # Write scans
    scanList = [int(analysis_id), version, module_name, sandbox_name, submitter,
                generation_date, int(total_scans), load_date]

    writeAccessScan(scanList)

    print("Scan count: %s" % total_scans)
    return total_scans, analysis_id


def getFlaws(xml_file, analysis_id):
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

            # Write flaws
            flawList = [int(analysis_id), ticket_id, int(severity), int(issueid), remediation_status,
                        int(cweid), categoryname, source_file, int(line_num), load_date]

            writeAccessFlaw(conn, flawList)
            row += 1

    conn.commit()
    conn.close()

    total_flaws = (row - 1)
    print ("Flaw count: %s" % total_flaws)
    return total_flaws

def writeAccessScan(scanList):
    # Insert into DB
    try:
        conn = pyodbc.connect(CONN_STR)
        cursor = conn.cursor()

        sql = "INSERT INTO scans(analysis_id, version, module_name, sandbox_name, submitter, " +\
            "generation_date, total_flaws, load_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

        cursor.execute(sql, scanList)
        conn.commit()
        conn.close()
    except pyodbc.Error as ex:
        print (ex)
        sys.exit(1)

def writeAccessFlaw(conn, flawList):
    # Insert into DB
    try:
        cursor = conn.cursor()

        sql = "INSERT INTO flaws(analysis_id, ticket_id, severity, issue_id, remediation_status, " +\
            "cwe_id, category_name, source_file, line_num, load_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

        cursor.execute(sql, flawList)
    except pyodbc.Error as ex:
        print (ex)
        sys.exit(1)

def main(xml_file):
    total_scans, analysis_id = getScans(xml_file)
    total_flaws = getFlaws(xml_file, analysis_id)

    if total_scans != total_flaws:
        print("Flaw counts do not match!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print ("Usage: " + sys.argv[0] + " xml_file")
        sys.exit(1)
        
    xml_file = sys.argv[1]
    main(xml_file)
