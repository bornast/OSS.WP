# -*- coding: utf-8 -*-
import socket
import time
import threading
import sys

received_message = ""
last_sent_message = ""
input_message = ""
send_message = False

def start_server():
    server_socket = get_server_socket()
    server_receive_messages(server_socket)

def get_server_socket():
    server_socket=socket.socket()

    host=socket.gethostname()
    port=int(sys.argv[1])

    server_socket.bind((host,port))
    server_socket.listen(3)

    return server_socket

def server_receive_messages(server_socket):
    global received_message, last_sent_message

    while True:
        client_socket, client_addr = server_socket.accept()
        received_message = (client_socket.recv(1024)).decode()   

def get_message_from_input():
    while True:
        global input_message
        global send_message

        input_message = raw_input()
        send_message = True

def send_message_to_next_node():
    global input_message, received_message, last_sent_message, send_message

    try:
        host = socket.gethostname()
        port = int(sys.argv[2])
        
        while True:
            time.sleep(5)

            # forward message
            if (last_sent_message != received_message and received_message != input_message):                
                send_message_to_server(host, port, received_message)
                last_sent_message = received_message
                print(received_message)

            # send message
            if (send_message == True):
                send_message_to_server(host, port, input_message)
                send_message = False
                last_sent_message = input_message

    except Exception as e:
        send_message_to_next_node()

def send_message_to_server(host, port, message):
    c = socket.socket()
    c.connect((host, port))
    c.send(message.encode())

threading._start_new_thread(start_server,())
threading._start_new_thread(get_message_from_input,())
send_message_to_next_node()
