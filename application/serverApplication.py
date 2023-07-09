# 1 thread -> receber a conexão dos edges
# 2 thread -> algoritmo de exclusão mútua distribuida
# 3 thread -> interface

import socket
import sqlite3
import threading
import queue
import time

HOST_SERVER_APPLICATION = 'localhost'
PORT_SERVER_APPLICATION = 3333

# fila de pedido
request_queue = queue.Queue()

# sincronizar o acesso a fila de pedido
mutex = threading.Lock()

request_count = {}

def login():
    connectionDB = sqlite3.connect('../database/db.db')
    cursor = connectionDB.cursor()

    command = "SELECT * FROM users"
    cursor.execute(command)
    result = cursor.fetchall()
    print(result)

def handle_connection(client_socket):
    while True:
        try:
            request = client_socket.recv(1024).decode()
            if not request:
                break

            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            print(f'{timestamp}: Mensagem recebida - {request}')

            with mutex:
                request_queue.put(request)
                process_id = request.split(',')[0]
                request_count[process_id] = request_count.get(process_id, 0) + 1

            # Simulação de processamento do pedido
            time.sleep(1)

            response = 'Pedido processado com sucesso'
            client_socket.send(response.encode())

            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            print(f'{timestamp}: Mensagem enviada - {response}')
        except:
            break

    client_socket.close()

def handle_interface():
    while True:
        command = input('Digite o comando (1 - Imprimir fila, 2 - Imprimir contagem, 3 - Encerrar): ')
        if command == '1':
            with mutex:
                print('Fila de Pedidos:')
                for item in request_queue.queue:
                    print(item)
                print()
        elif command == '2':
            with mutex:
                print('Contagem de Atendimentos:')
                for process_id, count in request_count.items():
                    print(f'Processo {process_id}: {count} vezes')
                print()
        elif command == '3':
            break

    # Encerrar a execução
    print('Encerrando a execução...')

def start_application_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST_SERVER_APPLICATION, PORT_SERVER_APPLICATION))
    server_socket.listen(2)

    print(f'Servidor de Aplicação iniciado em {HOST_SERVER_APPLICATION}:{PORT_SERVER_APPLICATION}')

    interface_thread = threading.Thread(target=handle_interface)
    interface_thread.start()

    while True:
        client_socket, client_address = server_socket.accept()
        connection_thread = threading.Thread(target=handle_connection, args=(client_socket,))
        connection_thread.start()

start_application_server()

# # iniciar socket server application
# server_application = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_application.bind(('localhost', 3333))
# server_application.listen()

# def edge_connection():
#     edge_connection, edge_address = server_application.accept()
#     message = edge_connection.recv(2048).decode()
#     print(message)

# if __name__ == "__main__":
#     threading.Thread(target=edge_connection).start()