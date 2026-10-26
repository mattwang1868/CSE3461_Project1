import sys
from socket import *
import threading

# function for receiving and sending message from each client
def communication(other_ip, other_port, other_socket, clients_list, clients_dict):
    client_username = None
    try:
        # request username from client
        client_socket.send(("Enter Username: ").encode())
        data = client_socket.recv(200)
        client_username = data.decode().strip()

        # add username to dictionary with key value
        clients_dict[client_username] = other_socket

        while True:
            # receive data
            data = other_socket.recv(200)
            message = data.decode()
            words = message.split()

            #ensure message is formatted correctly
            if (words[0][0] == '@'):
                target_username = words[0][1:]
                #if username exists send message
                if target_username in clients_dict:
                    clients_dict.get(target_username).send(("From " + client_username + ": " + message).encode())
                else:
                    other_socket.send(("Username not found").encode())
            # if no @
            else:
                # inform sender to use correct format
                other_socket.send(("Use format: \"@username message\"").encode())
    except KeyboardInterrupt:
        pass

    finally: #when sender ends connection
        print(f"Client {other_ip}, {other_port} has disconnected")
        # remove client from lists
        try: clients_dict.pop(client_username)
        except KeyError:
            print("Username doesn't exist")
        clients_list.remove(other_socket)
        other_socket.close()

#host and port
HOST = '0.0.0.0' 
PORT = 12033
# create socket
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((HOST,PORT))
# listen for connection requests
server_socket.listen()
clients_dict = {} # maps username and socket
clients_list = [] # list of client sockets
threads_list = [] # list of client threads
try:
    while True:
        # accept connection
        client_socket, client_address = server_socket.accept()

        # add to list
        clients_list.append(client_socket)

        # make thread to handle client
        client_thread = threading.Thread(target = communication, args = (client_address[0], client_address[1], client_socket, clients_list, clients_dict))
        threads_list.append(client_thread)
        client_thread.start()
except KeyboardInterrupt:
    # Close any open sockets
    server_socket.close()