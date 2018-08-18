import pyodbc

conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=Veracode.accdb;'
)

# conn_str = (
#     r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};Dbq=Veracode.accdb;'
#     r'Uid=Admin;Pwd=;'
# )

conn_str = (
    r'Provider=Microsoft.ACE.OLEDB.12.0;Data Source=C:\gDrive\BAR\veracode-load\Veracode.accdb;'
    r'Persist Security Info=False;'
)

cnxn = pyodbc.connect(conn_str)
crsr = cnxn.cursor()
for table_info in crsr.tables(tableType='TABLE'):
    print(table_info.table_name)
