import socket
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
    soc.bind(("", PORT))
    soc.listen()
    conn, addr = soc.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)