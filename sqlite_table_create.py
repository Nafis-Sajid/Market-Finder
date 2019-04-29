#This file should be executed if database file is lost or broken
import sqlite3

connection = sqlite3.connect("myTable.db")
crsr = connection.cursor()

sql_command = """CREATE TABLE Bank (  
    first VARCHAR(20),
    family VARCHAR(20),  
    postcode VARCHAR(20),
    creditcard VARCHAR(20) PRIMARY KEY,
    balance NUMBER(10),
    credit NUMBER(10)
    );"""

crsr.execute(sql_command)

#Insert 2 arbitary values
sql_command = (
    """INSERT INTO Bank VALUES ("Jim", "Morrison", "2052", "12345678", 100, 1000);"""
)

crsr.execute(sql_command)

sql_command = (
    """INSERT INTO Bank VALUES ("Eric", "Clapton", "2019", "53466207", 40, 500);"""
)

crsr.execute(sql_command)

connection.commit()

connection.close()
