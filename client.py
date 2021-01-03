import socket, ast

query= input("What is the query you would like to execute ?\n Examples: select('classroom','*')\nInput:")

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    if (len(query)>6):
        s.connect((HOST, PORT))
        s.sendall(query.encode())
        data = s.recv(1024)
        print('Received response from server\n', data.decode('utf8', 'strict'))
    else:
        print("Something wrong with your input!\n Please check the provided examples and try again :)")

