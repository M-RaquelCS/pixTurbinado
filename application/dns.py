import socket

dns_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dns_socket.bind(('localhost',53)) # porta padrão para requisição DNS
dns_socket.listen()
print("DNS iniciado.")

domains_dns_list = [
    {
      "www.pix.com.br": ('localhost', 3000)
    }
]

def request(connection_client):
    response = connection_client.recv(1024)
    domain = response.decode()
    print(domain)

    for domain_dns in domains_dns_list:
        if domain in domain_dns:
          ip, port = domain_dns[domain]
          message = (f"{ip}:{port}").encode()
          connection_client.send(message)

          print(f"IP: {ip}, PORT: {port}")
        else:
          print("Domínio não encontrado na lista.")

while True:
    connection_client, address_client = dns_socket.accept()
    print("Conexão estabelecida com o cliente: ", address_client)
    request(connection_client)