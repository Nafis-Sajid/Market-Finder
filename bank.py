# this program should be executed in
# the bank server pc
import sys
import socket
import json
import sqlite3

# a socket object
s = socket.socket()
print("Socket for Bank successfully created")

# reserve BANK_PORT from input argument for banking purpose
BANK_PORT = int(sys.argv[1])

# Bind to the BANK_PORT
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(("", BANK_PORT))
print("socket bound to ", BANK_PORT)

# put the socket into listening mode
s.listen(5)
print("socket is listening")
# for storing data
d = {}
received_info = {}

# funciton that does all the stuff
def banking():
    # Establish connection with client.
    c, addr = s.accept()
    print("Got data from", addr)

    # receive byte from server and decode it into string
    received = c.recv(1024).decode("utf-8")
    # convert into dictionary
    received_info = json.loads(received)


    # sqlite code for searching data goes here
    sqlite_connection = sqlite3.connect("myTable.db")
    crsr = sqlite_connection.cursor()
    fetch_command = (
        "SELECT balance, credit FROM Bank WHERE first = '"
        + received_info["first"]
        + "' AND family = '"
        + received_info["family"]
        + "' AND postcode = '"
        + received_info["postcode"]
        + "' AND creditcard = '"
        + received_info["creditcard"]
        + "'"
    )
    crsr = sqlite_connection.execute(fetch_command)

    validity = False
    for row in crsr:
        validity = True

    if validity:
        for idx, col in enumerate(crsr.description):
            d[col[0]] = row[idx]

    # close sqlite connection
    sqlite_connection.close()


    # check user input validities
    if not validity:
        c.send(bytes("The user information entered is invalid", "utf-8"))

    # check if user has sufficient balance
    elif d["credit"] < received_info["cost"]:
        c.send(
            bytes(
                "Your account does not have sufficient credit for the requested transaction",
                "utf-8",
            )
        )

    # passed all checks
    else:
        c.send(bytes("Transaction Approved", "utf-8"))
        #update variables
        d["credit"] -= received_info["cost"]
        d["balance"] += received_info["cost"]

        # sqlite code goes here
        sqlite_connection = sqlite3.connect("myTable.db")
        update_command = (
            "UPDATE Bank SET balance = '"
            + str(d["balance"])
            + "', credit = '"
            + str(d["credit"])
            + "' where creditcard = '"
            + received_info["creditcard"]
            + "'"
        )
        sqlite_connection.execute(update_command)
        sqlite_connection.commit()
        sqlite_connection.close()

    # Close the connection with the client
    c.close()
    


# main function
if __name__ == "__main__":
    # a forever loop until we interrupt it or an error occurs
    while True:
        banking()
