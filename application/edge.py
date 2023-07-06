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


def is_port_in_use(port):
    try:
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.bind(('localhost', port))
        test_socket.close()
        return False
    except OSError:
        return True


def handle_client_request(client_socket):
    request = pickle.loads(client_socket.recv(2048))

    if request_mold.match(request) and request.split('|')[0] == '1':
        mutex.acquire()  # Adquirir o mutex antes de acessar o servidor de dados

        edge_server = select_edge_server()
        response = send_request_to_edge_server(edge_server, request)

        print(f'edge compute: {response}')
        if response.split('|')[1] == '1':
            client_socket.sendall(response.encode())

        mutex.release()  # Liberar o mutex após acessar o servidor de dados

    # Resto do código...

def select_edge_server():
    # Implemente aqui a lógica para selecionar um servidor de Edge Computing
    # Neste exemplo, um servidor é selecionado de forma aleatória
    return random.choice(edge_servers)

def send_request_to_edge_server(edge_server, request):
    # Envie a solicitação para o servidor de Edge Computing selecionado
    try:
        edge_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        edge_socket.connect(edge_server)
        edge_socket.sendall(request.encode())

        response = edge_socket.recv(2048).decode()
        edge_socket.close()
        return response
    except socket.error as e:
        print(f"Erro ao enviar a requisição para o servidorde Edge Computing: {str(e)}")

# Resto do código...

# Iniciar o servidor de aplicação
if is_port_in_use(PORT):
    PORT += 1
    application_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    application_server.bind((HOST, PORT))
    application_server.listen()
else:
    application_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    application_server.bind((HOST, PORT))
    application_server.listen()

print(f'Servidor iniciado em {HOST}:{PORT}')

while True:
    client_socket, _ = application_server.accept()
    threading.Thread(target=handle_client_request, args=(client_socket,)).start()
