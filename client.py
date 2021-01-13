import socket
import ast
import pickle

query = input(
    "What is the query you would like to execute ?\n Examples: select('classroom','*')\nInput: ")
nextQuery = None  # At first it will be empty to trigger the question on the client if he wishes to execute more than one query but if it sets a value it won't be asked again

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    while True:
        if nextQuery is None: # For first run 
            s.connect((HOST, PORT))
            s.sendall(query.encode())
            data = s.recv(1024)
            print('Received response from server\n',
                  data.decode('utf8', 'strict'))
            nextQuery = input(
                "Would you like to execute something else ?[y/n]\nIf you later wish to exit the program don't enter anything in your input and press Enter...\nInput:")
            query = nextQuery
        else:
            print(
                "Something1 wrong with your input!\n Please check the provided examples and try again :)")
            s.close()
            exit()

        if query != "":
            s.sendall(query.encode())
            data = s.recv(1024)
            print('Received response from server\n',
                    data.decode('utf8', 'strict'))
            query = input(
                "Would you like to execute something else ?[y/n]\nIf you later wish to exit the program don't enter anything in your input and press Enter...\nInput:")
            continue
        else:
            print(
                "Something2 wrong with your input!\n Please check the provided examples and try again :)")
            s.close()
            exit()
        

# elif nextQuery == "y" or nextQuery == "Y":
#             query = input(
#                 "What is the query you would like to execute ?\n Examples: select('classroom','*')\nInput:")