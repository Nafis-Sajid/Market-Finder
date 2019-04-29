#This file should be executed if database file is lost or broken
import sqlite3

connection = sqlite3.connect("myTable.db")
crsr = connection.cursor()

sql_command = """CREATE TABLE User (
    name VARCHAR(20),
    email VARCHAR(30) PRIMARY KEY,
    password VARCHAR(15),
    location VARCHR(70),
    mobile VARCHAR(11)
    );"""

crsr.execute(sql_command)
connection.commit()

connection.close()
