#run this code to view the whole table
import sqlite3
connection = sqlite3.connect("myTable.db")
crsr = connection.cursor()
crsr = connection.execute("SELECT * FROM Bank")
for row in crsr:
    print(row)
# close sqlite connection
connection.close()