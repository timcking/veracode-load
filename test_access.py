import pyodbc

conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=.\\VeracodeJuly.accdb;'
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# cursor.execute("SELECT COUNT(*) FROM flaws")
# num_flaws = cursor.fetchone()
# print (num_flaws)
scanList = [int(1234567), "This is version"]

sql = "INSERT INTO scans(analysis_id, version) VALUES (?, ?)"

cursor.execute(sql, scanList)
conn.commit()

sql = "SELECT * FROM scans"

cursor.execute(sql)
for row in cursor.fetchall():
    print (row)

for table_info in cursor.tables(tableType='TABLE'):
    print(table_info.table_name)

conn.close()