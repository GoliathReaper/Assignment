import sqlite3

conn1 = sqlite3.connect('database1.db')
cursor1 = conn1.cursor()
cursor1.execute('''CREATE TABLE IF NOT EXISTS table1 (
                   column1 INTEGER, column2 INTEGER, column3 INTEGER,
                   column4 INTEGER, column5 INTEGER, column6 INTEGER)''')
conn1.commit()
conn1.close()

conn2 = sqlite3.connect('database2.db')
cursor2 = conn2.cursor()
cursor2.execute('''CREATE TABLE IF NOT EXISTS table2 (
                   column21 INTEGER, column22 INTEGER, column23 INTEGER,
                   column24 INTEGER, column25 INTEGER, column26 INTEGER)''')
conn2.commit()
conn2.close()
