import sys
from socket import *
import threading

# get messages from server and display them
def get_messages():
    # receive message and print it
    while True:
        message = client_socket.recv(200)
        print(message.decode())
    return

# server ip and port
SERVER_IP = "0.0.0.0" #TODO: change to IP of local machine
SERVER_PORT = 12033

# Create a socket for the sender
client_socket=socket(AF_INET, SOCK_STREAM)

# connect client to server
client_socket.connect((SERVER_IP, SERVER_PORT))

# wait until server requests username
message = client_socket.recv(200).decode()

# send username to server
if message == "Enter Username: ":
    username = input(message)
    client_socket.send(username.encode())

# create thread to get data from server
listen_thread = threading.Thread(target=get_messages, args=())
listen_thread.start()

# take input and send to server
while True:
    try:
        message = input()
        client_socket.send(message.encode())
    except KeyboardInterrupt:
        # close socket
        client_socket.close()