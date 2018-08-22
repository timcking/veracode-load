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

sql = "INSERT INTO scans(analysis_id, version) VALUES (?, ?)"

cursor.execute(sql, 12345, 'awesome library')
conn.commit()

sql = "SELECT * FROM scans"

cursor.execute(sql)
for row in cursor.fetchall():
    print (row)

for table_info in cursor.tables(tableType='TABLE'):
    print(table_info.table_name)

conn.close()