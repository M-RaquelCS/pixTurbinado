import socket
import re
from time import sleep
import threading  # Importar o módulo threading para usar mutex
import random
import pickle

HOST = 'localhost'
PORT = 5000
F = 2048  # Tamanho fixo da mensagem em bytes

edge_servers = [
    ('localhost', 5000),
    ('localhost', 5001),
    ('localhost', 5002)
]

request_mold = re.compile(r'^[1-9]\|[0-9]{1,8}\|[0-9]{1,3}\|[0-9]{1,8}\|[0-9]{1,11}$')

mutex = threading.Lock()  # Inicializar o mutex

sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sckt.bind((HOST, PORT))
sckt.listen()

client_socket, _ = sckt.accept()

resquest = client_socket.recv(F).decode()
print(resquest)

# def is_port_in_use(port):
#     try:
#         test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         test_socket.bind(('localhost', port))
#         test_socket.close()
#         return False
#     except OSError:
#         return True
    
# if is_port_in_use(PORT):
#     PORT += 1
#     application_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     application_server.bind((HOST, PORT))
#     application_server.listen()
# else:
#     application_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     application_server.bind((HOST, PORT))
#     application_server.listen()

# print(f'Servidor iniciado em {HOST}:{PORT}')

# while True:
#     client_socket, _ = sckt.accept()
#     threading.Thread(target=handle_client_request, args=(client_socket,)).start()