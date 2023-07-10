import socket
import psutil #Biblioteca para interagir com o sistema operacional. nesse caso, para pegar o PID do processo.
import threading #para lidar com múltiplas conexões em paralelo

F = 2048  # Tamanho fixo da mensagem em bytes

HOST_EDGE = 'localhost' #
PORT_EDGE = 5000

MAX_EDGE_SERVERS = 3

HOST_SERVER_APPLICATION = 'localhost'
PORT_SERVER_APPLICATION = 3333

def using_port(port):
    for connection in psutil.net_connections():
        if connection.laddr.port == port and connection.status == 'LISTEN':
            return True
    return False

def start_edge_server(port):
    edge_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    edge_socket.bind((HOST_EDGE, port))
    edge_socket.listen()
    print(f'Edge iniciado em {HOST_EDGE}:{port}')

    while True:
        client_connection, client_address = edge_socket.accept()
        print("Cliente conectado ao edge da porta:", port)
        threading.Thread(target=handle_request, args=(client_connection,)).start()

def handle_request(client_connection):
    request = client_connection.recv(F).decode()
    print(request)

    server_application = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_application.connect((HOST_SERVER_APPLICATION, PORT_SERVER_APPLICATION))
    server_application.send(request.encode())

    response = server_application.recv(F).decode()
    print(response)

    client_connection.send(response.encode())

    server_application.close()
    
#verifica se o script está sendo executado como um programa principal. 
if __name__ == "__main__":
    for port in range(PORT_EDGE, PORT_EDGE + MAX_EDGE_SERVERS): # 5000 , 5000 + 3 = 5002
        if not using_port(port): # False
            threading.Thread(target=start_edge_server, args=(port,)).start() # 5000