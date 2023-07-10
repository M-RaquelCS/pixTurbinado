# 1 thread -> receber a conexão dos edges
# 2 thread -> algoritmo de exclusão mútua distribuida
# 3 thread -> interface

import socket
import sqlite3
import threading
import queue
import time
import message_constructor

HOST_SERVER_APPLICATION = 'localhost'
PORT_SERVER_APPLICATION = 3333

F = 27

# fila de pedido
request_queue = queue.Queue() #Criação de uma fila de pedidos usando queue.Queue(). A fila será usada para armazenar os pedidos recebidos dos edges.

# sincronizar o acesso a fila de pedido
mutex = threading.Lock()

request_count = {}

def write_file(text):
    with open('log.txt', 'a') as file:
        file.write(text)

def login(request_message,client_socket):
    connectionDB = sqlite3.connect('E:\SD\pixTurbinado\database\db.db')
    cursor = connectionDB.cursor()

    pid = request_message.split('|')[1]

    agency = request_message.split('|')[2]
    account_number = request_message.split('|')[3]

    command = "SELECT * FROM users WHERE agency = ? AND account_number = ?"
    data_client = (agency, account_number)
    cursor.execute(command, data_client)

    result = cursor.fetchall() # [[]]
    # print(result)
    if len(result) > 0:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        write_file(f'{timestamp}: Client access account - PID: {pid}\n')

        with mutex:
            request_count[pid] = request_count.get(pid, 0) + 1
        
        login_message = message_constructor.message(6, pid, agency, account_number, 0)
        client_socket.send(login_message.encode())
        
    else:
        no_login_message = message_constructor.message(6, pid, 0, 0, 0)
        client_socket.send(no_login_message.encode())
        client_socket.close()

def pix(request_message,client_socket):
    connectionDB = sqlite3.connect('E:\SD\pixTurbinado\database\db.db')
    cursor = connectionDB.cursor()

    pid = request_message.split('|')[1]
    origin_transaction = request_message.split('|')[2]
    destination_transaction = request_message.split('|')[3]
    value_transaction = request_message.split('|')[4].lstrip('0')

    command_verify_balance = 'SELECT balance FROM users WHERE account_number = ?'
    cursor.execute(command_verify_balance, (origin_transaction,))

    result = cursor.fetchall()
    if len(result) > 0 and result[0][0] >= int(value_transaction): # [[20]] -> 30
        command_update_balance_origin = 'UPDATE users SET balance = balance - ? WHERE account_number = ?'
        data_update_balance_origin = (value_transaction, origin_transaction)

        cursor.execute(command_update_balance_origin, data_update_balance_origin)
        connectionDB.commit()

        command_update_balance_destination = 'UPDATE users SET balance = balance + ? WHERE account_number = ?'
        data_update_balance_destination = (value_transaction, destination_transaction)
        
        cursor.execute(command_update_balance_destination, data_update_balance_destination)
        connectionDB.commit()

        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        write_file(f'{timestamp}: {origin_transaction} transfers to {destination_transaction} - PID: {pid}\n')
        write_file(f'{timestamp}: {destination_transaction} received to {origin_transaction} - PID: {pid}\n')
        
        pix_message = message_constructor.message(4, pid, origin_transaction, 0, 0)
        client_socket.send(pix_message.encode())

        with mutex:
            request_count[pid] = request_count.get(pid, 0) + 1
            if not request_queue.empty():
                item = request_queue.get(pid)
                write_file(f'{timestamp}: Removed client - PID: {pid} | {item}\n')

    else:
        write_file(f'{timestamp}: {origin_transaction} failed to transfer to {destination_transaction} - PID: {pid}\n')
        with mutex:
            if not request_queue.empty():
                item = request_queue.get(pid)
                write_file(f'{timestamp}: Removed client - PID: {pid} | {item}\n')


def handle_connection(client_socket):
    request_message = client_socket.recv(F).decode() # 5|002780|0000|0000|00000000

    if request_message.split('|')[0] == '5':
        pid = request_message.split('|')[1]

        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        write_file(f'{timestamp}: Client is connected - PID: {pid}\n')

        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        write_file(f'{timestamp}: Server recognized connection to client - PID: {pid}\n')
        permission_message = message_constructor.message(6, pid, 0, 0, 0)
        client_socket.send(permission_message.encode())

        with mutex:
            request_queue.put(pid)
            request_count[pid] = request_count.get(pid, 0) + 1

    elif request_message.split('|')[0] == '6':
        login(request_message,client_socket)
    
    elif request_message.split('|')[0] == '3':
        pix(request_message,client_socket)

        # # Simulação de processamento do pedido
        # time.sleep(1)

        # login(request_message, client_socket)

        # response = 'Pedido processado com sucesso'
        # client_socket.send(response.encode())

        # timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        # write_file(f'{timestamp}: Mensagem enviada\n')

    # client_socket.close()

def handle_interface():
    while True:
        command = input('Digite o comando' 
                        '\n1 - Imprimir fila' 
                        '\n2 - Imprimir contagem' '\n3 - Encerrar' 
                        '\n-> ')
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
    server_socket.listen()

    print(f'Servidor de Aplicação iniciado em {HOST_SERVER_APPLICATION}:{PORT_SERVER_APPLICATION}')

    interface_thread = threading.Thread(target=handle_interface)
    interface_thread.start()

    while True:
        client_socket, client_address = server_socket.accept()
        connection_thread = threading.Thread(target=handle_connection, args=(client_socket,))
        connection_thread.start()

start_application_server()

#tentativa de implementar uma conexão com os edges
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