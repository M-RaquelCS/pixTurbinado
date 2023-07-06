import socket
import pickle

F = 2048

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
  balancer_socket.connect((address[0], address[1]))
  print("Conectado ao balancer")

  # array_decoder = pickle.dumps(address)
  balancer_socket.send(request.encode())
  response = balancer_socket.recv(F).decode()
  balancer_socket.close()
  return response

domain = input("Escreva seu domínio: ")
address = get_address(domain)

# 
send_balance(address)