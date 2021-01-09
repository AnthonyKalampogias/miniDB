from database import Database
import socket
import sys
from io import StringIO


HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


# Function to run when a clinet connects to the server

def clientConnect(receivedData, data):
    #receivedData is a flag that tells the function to either wait for input(first run from client) line 21
    # or either tell it that I have a new input from the client so just execute that
    # data is the variable that I store the desired query and it contains a value only when the function is recursivly called

    sendToClient = False  # if true the server will send the response to the client
    print('Connected by', addr)

    if receivedData:  # If this is the first query, wait for input
        data = conn.recv(1024)  # Receive query
        data = data.decode("utf-8")  # Decode it
        data = data.lower()  # Sanitize user input to check what he wants to execute

    if "database" in data:  # Check if the user wants to create a database
        data = data.split("'")
        db = Database(data[1], load=False)
    else:
        # create db with name "clientCB"
        db = Database('clientCB', load=False)
        FinalQuery = "db.{}".format(data)
        # Add to a variable with the db object along with the received query from the client
        print("Client {} requested to execute the query {}".format(addr, FinalQuery))

        old_stdout = sys.stdout
        result = StringIO()
        sys.stdout = result
        # Above 3 lines are standard to save the stdout that python uses with print()
        # inside the variable result

        if len(FinalQuery) > 3:  # Contains more than just "db." the object
            exec(FinalQuery)  # Execute the query
            sendToClient = True
        if not sendToClient:
            print("Something went wrong..\n")

        else:
            sys.stdout = old_stdout
            result_string = result.getvalue()
            print(result_string)
            conn.sendall(str.encode(result_string))
            data = conn.recv(1024)  # Receive query
            data = data.decode("utf-8")  # Decode it
            if data != "":
                # Recursivly call it's self with setting the receivedData flag to false so it won't wait again for input
                clientConnect(False, data)
                    # receivedData -> False, there is already available data to execute
                    # data -> Now has the received data from the client
            else:
                print("Empty Input!!!\nTerminating connection...")
                conn.close()


while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            clientConnect(True, None)  
                # receivedData -> True, First Run
                # data -> None, Since it is the first run no data is available
            s.close()
            print(
                "Clients valid queries were executed\nDropping connection..\nWaiting for next connection...\n")
            continue  # Break out and wait for next connection
