from database import Database
import socket
import sys
from io import StringIO


# create db with name "smdb"
db = Database('vsmdb', load=False)

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

#Function to run when a clinet connects to the server
def clientConnect():
    sendToClient= False # if true the server will send the response to the client
    print('Connected by', addr)
    
    while True:
        
        data = conn.recv(1024) # Receive query
        data = data.decode("utf-8") # Decode it
        # Add to a variable with the db object along with the received query from the client
        FinalQuery= "db.{}".format(data)
        print("Client {} requested to execute the query {}".format(addr,FinalQuery))
        
        old_stdout = sys.stdout
        result = StringIO()
        # Above 3 lines are standard to save the stdout that python uses with print()
        # inside the variable result
        sys.stdout = result
        
        if len(FinalQuery) >3: #Contains more than just "db." the object
            exec(FinalQuery) # Execute the query 
            sendToClient= True
        if not sendToClient:
            print("Something went wrong..\n")
            break
        else:
            sys.stdout = old_stdout            
            result_string = result.getvalue()
            print(result_string)
            conn.sendall(str.encode(result_string))
            conn.close()
            break    

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            clientConnect() # Call the function that will execute the clients query and send him back the response
            print("Clients query executed\nDropping connection..\nWaiting for next connection...\n")
            continue # Break out and wait for next connection

