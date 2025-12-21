import socket
from . import config

def create_connection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((config.HOST, config.PORT))
    return s

def send_message(sock, message_bytes):
    sock.sendall(message_bytes)

def receive_message(sock, buffer_size=8192):
    return sock.recv(buffer_size)

def start_server_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((config.HOST, config.PORT))
    s.listen()
    return s
