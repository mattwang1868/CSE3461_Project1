
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
SERVER_IP = "10.193.105.135" # should be changed accordingly depending on server's IP
SERVER_PORT = 12035

# Create a socket for the sender
client_socket=socket(AF_INET, SOCK_STREAM)

# connect client to server
client_socket.connect((SERVER_IP, SERVER_PORT))

# wait for server to accept
input("Press enter to start transmissions")

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
