import socket
import os
import message_constructor

F = 2048
process_id = str(os.getpid()).zfill(6) # intervalo de 0  a 999999

def get_address(domain):
  dns_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  dns_socket.connect(('localhost',53))
  print("Conectado ao DNS")

  dns_socket.send(domain.encode())

  response_address = dns_socket.recv(1024).decode()
  dns_socket.close()
  return response_address.split(':') # 'localhost:3000' -> ['localhost', 3000]
    
def send_balance(address, request):
  balancer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  balancer_socket.connect((address[0], int(address[1]))) # conexão com o IP e PORT recebido pelo DNS
  print("Conectado ao Balanceador")

  balancer_socket.send(request.encode()) # envio da mensagem de resquisição (a primeira é um aviso de que o client está conectado)
  response = balancer_socket.recv(F).decode() # recebo uma resposta vinda do balanceador sobre minha requisição
  balancer_socket.close()
  return response

domain = input("Escreva seu domínio: ")

# messagem para "avisar" que o client está conectado
message_connected = message_constructor.message(5, process_id, 0, 0, 0)
address = get_address(domain)

send_balance(address, message_connected)