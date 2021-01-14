from database import Database
import socket
import sys
from io import StringIO
import SQLcompiler


HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


# Function to run when a clinet connects to the server

def clientConnect(receivedData, data, oldDatabase):
    #receivedData is a flag that tells the function to either wait for input(first run from client) line 21
    # or either tell it that I have a new input from the client so just execute that
    # data is the variable that I store the desired query and it contains a value only when the function is recursively called

    sendToClient = False  # if true the server will send the response to the client

    print('Connected by', addr)

    try:
        if receivedData:  # If this is the first query, wait for input
            data = conn.recv(1024)  # Receive query
            data = data.decode("utf-8")  # Decode it
            data = data.lower()
            data2 = data.split(" ")
            try:
                if "use" in data2:
                    db, msg = SQLcompiler.sqlCompiler(data)
                else:
                    db = None
                    db, msg = SQLcompiler.sqlCompiler(data,db)
            except:
                conn.sendall("Something went wrong with your input..")
                conn.close()
        else:
            db, msg = SQLcompiler.sqlCompiler(data,oldDatabase)
    except:
        conn.sendall("Something went wrong with your input..")
        conn.close()

    print(msg)
    conn.sendall(str.encode(msg))
    data = conn.recv(1024)  # Receive query
    data = data.decode("utf-8")  # Decode it
    print(data)
    if data != "":
        # Recursivly call it's self with setting the receivedData flag to false so it won't wait again for input
        clientConnect(False, data, db)
            # receivedData -> False, there is already available data to execute
            # data -> Now has the received data from the client
    else:
        print("Empty Input!!!\nTerminating connection...")
        conn.close()

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        global db 
        conn, addr = s.accept()
        with conn:
            clientConnect(True, None, None)  
                # receivedData -> True, First Run
                # data -> None, Since it is the first run no data is available
            s.close()
            print(
                "Clients valid queries were executed\nDropping connection..\nWaiting for next connection...\n")
            continue  # Break out and wait for next connection
