import os
import message_constructor

process_id = str(os.getpid()).zfill(6) # intervalo de 0  a 999999

message_connected = message_constructor.message(5, process_id, 0, 0, 0)
print(message_connected)

# def handle_request(client_connection):
#     request = client_connection.recv(F).decode()
#     print(request)

    # server_application = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_application.connect((HOST_SERVER_APPLICATION, PORT_SERVER_APPLICATION))
    # server_application.send(request.encode())

# def send_request_to_edge_server(edge_server, request):
#     # Envie a solicitação para o servidor de Edge Computing selecionado
#     try:
#         edge_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         edge_socket.connect(edge_server)
#         edge_socket.sendall(request.encode())

#         response = edge_socket.recv(2048).decode()
#         edge_socket.close()
#         return response
#     except socket.error as e:
#         print(f"Erro ao enviar a requisição para o servidorde Edge Computing: {str(e)}")

# def select_edge_server():
#     # Implemente aqui a lógica para selecionar um servidor de Edge Computing
#     # Neste exemplo, um servidor é selecionado de forma aleatória
#     return random.choice(edge_servers)

# def handle_client_request(client_socket):
#     request = client_socket.recv(2048)
#     print(request)

#     if request_mold.match(request) and request.split('|')[0] == '1':
#         mutex.acquire()  # Adquirir o mutex antes de acessar o servidor de dados

#         edge_server = select_edge_server()
#         response = send_request_to_edge_server(edge_server, request)

#         print(f'edge compute: {response}')
#         if response.split('|')[1] == '1':
#             client_socket.sendall(response.encode())

#         mutex.release()  # Liberar o mutex após acessar o servidor de dados