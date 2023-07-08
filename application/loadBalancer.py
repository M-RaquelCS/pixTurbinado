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
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    # dados da conexão com o socket edge
    # pega os valores da primeira posição do array, o retirando do array
    edge_address = list_edge_servers_queue.pop(0)
    print(edge_address) 

    try:
        request = connection_client_resquesting.recv(1024) # localhost:3000
        print(request)

        print("foi")
        sckt.connect(edge_address)
        sckt.send(request)
        
    finally:
        print("foi part 2")
        sckt.close()
        list_edge_servers_queue.append(edge_address)
    

while True:
    connection_client, address_client = balancer_socket.accept()
    print("Conexão estabelecida com o cliente: ", address_client)

    load_balancer(connection_client)