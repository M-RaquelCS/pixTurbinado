import socket

balancer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
balancer_socket.bind(('localhost', 3000))
balancer_socket.listen()
print("Balanceador iniciado.")

edge_servers = [
    ('localhost', 5000),
    ('localhost', 5001),
    ('localhost', 5002)
]

list_edge_servers_queue = list(edge_servers) # cria uma cópia da lista e atribui nessa variável

def load_balancer(connection_client_resquesting):
    edge_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    try:
        request = connection_client_resquesting.recv(1024) # recebendo a requisição
        print(request)

        # dados da conexão com o socket edge
        # pega os valores da primeira posição do array, o retirando do array
        edge_address = list_edge_servers_queue.pop(0)
        print(edge_address)

        edge_socket.connect(edge_address)
        edge_socket.send(request)
        print("foi")
        
    finally:
        edge_socket.close()
        list_edge_servers_queue.append(edge_address)
        print("foi part 2")
    

while True:
    connection_client, address_client = balancer_socket.accept()
    print("Conexão estabelecida com o cliente: ", address_client)

    load_balancer(connection_client)