import socket
import pytest
from threading import Thread


@pytest.fixture(scope='class', autouse=True)
def setup_dns_server(request):
    # Configuração do servidor DNS
    HOST = 'localhost'
    PORT = 53
    F = 28

    dns_table = {
        'www.example.com': ('127.0.0.1', 3000)
    }

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    # Iniciar o servidor DNS em uma thread separada
    server_thread = Thread(target=start_dns_server, args=(server_socket, dns_table, F))
    server_thread.start()

    def teardown():
        # Encerrar o servidor DNS e aguardar a conclusão da thread
        server_socket.close()
        server_thread.join()

    request.addfinalizer(teardown)


def start_dns_server(server_socket, dns_table, F):
    while True:
        connection, address = server_socket.accept()
        handle_dns_request(connection, dns_table, F)


def handle_dns_request(client_socket, dns_table, F):
    data = client_socket.recv(F) # link -> www.exemplo.com
    domain = data.decode().strip()

    if domain in dns_table:
        ip, port = dns_table[domain]
        response = f"{ip}:{port}"
    else:
        response = "Domain not found"

    client_socket.sendall(response.encode())
    client_socket.close()


class TestDNSServer:
    @pytest.mark.asyncio
    async def test_existing_domain(self, setup_dns_server):
        # Conectar ao servidor DNS e enviar uma solicitação para um domínio existente
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 53))
        client_socket.sendall('www.example.com'.encode())

        # Receber a resposta do servidor DNS
        response = client_socket.recv(28).decode()

        # Verificar se a resposta está correta
        assert response == '127.0.0.1:3000'

        # Fechar o socket do cliente
        client_socket.close()

    @pytest.mark.asyncio
    async def test_nonexistent_domain(self, setup_dns_server):
        # Conectar ao servidor DNS e enviar uma solicitação para um domínio inexistente
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 53))
        client_socket.sendall('nonexistent.com'.encode())

        # Receber a resposta do servidor DNS
        response = client_socket.recv(28).decode()

        # Verificar se a resposta está correta
        assert response == 'Domain not found'

        # Fechar o socket do cliente
        client_socket.close()
