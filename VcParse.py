import xml.etree.ElementTree as ET
import sys
from datetime import datetime
import logging
import Database as db
import pyodbc

# Every object in the tree has this at the beginning
URL = "{https://www.veracode.com/schema/reports/export/1.0}"

CONN_STR = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=.\\data\\Veracode.accdb;'
)

# Timestamp
load_date = datetime.now()

def getScans(xml_file):
    # Setup logging
    logName = xml_file.replace(".xml", ".log").replace("xml/", "log/")
    logging.basicConfig(filename=logName, format='%(levelname)s: %(message)s', filemode='w', level=logging.DEBUG)

    conn = pyodbc.connect(CONN_STR)
    
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

        # Translate the Veracode date/time
        generation_date = datetime.strptime(str_gen_date, '%Y-%m-%d %H:%M:%S %Z')

    for sa in root.findall("./" + URL + "static-analysis"):
        version = sa.attrib["version"]

    strNode = "./" + URL + "static-analysis/" + URL + "modules/" + URL + "module"
    for flaw in root.findall(strNode):
        module_name = flaw.attrib["name"]

    # Check for existing
    queryParams = [analysis_id]
    scanCount = db.getScanCount(conn, queryParams)
            
    # Does not overwrite existing scans
    if scanCount > 0:
        logging.info("IGNORING existing scan for analysis_id %s, sandbox_id %s " % (str(analysis_id), str(sandbox_id)))
        return -1, analysis_id, sandbox_id
    else:
        # Write scans to database
        scanList = [int(analysis_id), int(sandbox_id), version, module_name, sandbox_name, submitter,
                    generation_date, int(total_scans), load_date, xml_file.replace("xml/", "")]

        db.insertScan(conn, scanList)

    logging.info("Scan count: %s" % total_scans)
    return total_scans, analysis_id, sandbox_id

def getFlaws(xml_file, analysis_id, sandbox_id):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    conn = pyodbc.connect(CONN_STR)

    # Write flaws
    row = 1
    fixed = 0
    
    strNode = "./" + URL + "severity/" + URL + "category/" + URL + "cwe/" + URL + "staticflaws/" + URL + "flaw"
    for cwe in root.findall(strNode):
        remediation_status = (cwe.attrib["remediation_status"])

        flaw_id = (cwe.attrib["issueid"])
        # Convert sev numbers into high, low, etc
        severity = (switchSeverity(cwe.attrib["severity"]))
        cweid = (cwe.attrib["cweid"])
        categoryname = (cwe.attrib["categoryname"])
        source_file = (cwe.attrib["sourcefile"])
        line_num = (cwe.attrib["line"])
        
        # Placeholder for linking with tickets
        ticket_id = None

        # Commented out code will overwrite existing flaws with new analysis_id if sandbox is the same
        # Check for existing
        #queryParams = [analysis_id, sandbox_id, flaw_id]
        #flawCount = db.getFlawCount(conn, queryParams)

        #if (flawCount > 0):
            ## Update
            #flawList = [remediation_status, load_date, int(analysis_id), int(sandbox_id), int(flaw_id)]
            #db.updateFlaw(conn, flawList)
        #else:
        
        # Insert
        update_date = None
        flawList = [int(analysis_id), int(sandbox_id), ticket_id, severity, int(flaw_id), remediation_status,
                    int(cweid), categoryname, source_file, int(line_num), load_date, update_date]
        db.insertFlaw(conn, flawList)
        
        queryParams = [int(analysis_id), int(sandbox_id), int(flaw_id)]
        priorFlawCount = db.getPriorFlawCount(conn, queryParams)
    
        # Need to track fixed separately
        if remediation_status == "Fixed":
            fixed += 1
        else:
            row += 1

    conn.commit()
    conn.close()

    total_flaws = (row - 1)
    logging.info ("Flaw count: %s" % total_flaws)
    logging.info ("Fixed count: %s" % fixed)

    logging.disable()
    
    return total_flaws

def switchSeverity(sev_num):
     # Convert sev numbers into high, low, etc
    return {
        '0': 'Notification',
        '1': 'Very Low',
        '2': 'Low',
        '3': 'Medium',
        '4': 'High',
        '5': 'Very High'
    }[sev_num]

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
