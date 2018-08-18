import xml.etree.ElementTree as ET
import xlsxwriter
import sys

# Every object in the tree has this at the beginning
URL = "{https://www.veracode.com/schema/reports/export/1.0}"
xml_file = ""

def getScans():
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Need to get analysis_id first
    for dr in root.iter(URL + "detailedreport"):
        analysis_id = int(dr.attrib["analysis_id"])
        total_flaws = int((dr.attrib["total_flaws"]))
        generation_date = dr.attrib["generation_date"]

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook("scans_" + str(analysis_id) + ".xlsx")
    worksheet = workbook.add_worksheet()

    # Write scans header
    scanHeaderList = ['analysis_id', 'version', 'module_name', 'generation_date', 'total_flaws']
    col = 0
    for item in scanHeaderList:
        worksheet.write(0,col, item)
        col += 1

    for sa in root.findall("./" + URL + "static-analysis"):
        version = sa.attrib["version"]

    strNode = "./" + URL + "static-analysis/" + URL + "modules/" + URL + "module"
    for flaw in root.findall(strNode):
        module_name = flaw.attrib["name"]

    # Write scans
    scanList = [int(analysis_id), version, module_name, generation_date, int(total_flaws)]
    col = 0
    for item in scanList:
        worksheet.write(1,col, item)
        col += 1

    workbook.close()
    print("Scan count: %s" % total_flaws)

    return int(analysis_id)

def getFlaws(analysis_id):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook("flaws_" + str(analysis_id) + ".xlsx")
    worksheet = workbook.add_worksheet()

    # Write flaws header
    flawHeaderList = ['analysis_id', 'citrix_ticket_id', 'severity', 'issue_id', 'remediation_status',
                      'cwe_id', 'category_name', 'source_file', 'line_num']
    col = 0
    for item in flawHeaderList:
        worksheet.write(0, col, item)
        col += 1

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
            citrix_ticket_id = None

            # Write flaws
            flawList = [int(analysis_id), citrix_ticket_id, int(severity), int(issueid), remediation_status,
                        int(cweid), categoryname, source_file, int(line_num)]
            col = 0
            for item in flawList:
                worksheet.write(row, col, item)
                col += 1

            row += 1

    workbook.close()

    print ("Flaw count: %s" % str(row - 1))

def main():
    analysis_id = getScans()
    getFlaws(analysis_id)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print ("Usage: " + sys.argv[0] + " xml_file")
        sys.exit(1)
        
    xml_file = sys.argv[1]
    main()
