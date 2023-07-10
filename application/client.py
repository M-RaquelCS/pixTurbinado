import socket
import os # Biblioteca para interagir com o sistema operacional. nesse caso, para pegar o PID do processo.
import message_constructor #Módulo personalizado que contém a função message() para construir mensagens.

F = 2048 #Tamanho máximo do buffer de recepção dos sockets.

#Obtém o ID do processo atual e o preenche com zeros à esquerda para ter sempre 6 dígitos.
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

domain = input("Escreva seu domínio: ") # domínio do client.. Solicitação do domínio ao usuário através da função input().

# messagem para "avisar" que o client está conectado
# 5 é o código que indica uma mensagem de conexão.
# process_id é o ID do processo do cliente.
# Os três últimos zeros são valores de dados específicos da mensagem (neste caso, não utilizados).
message_connected = message_constructor.message(5, process_id, 0, 0, 0) 
address = get_address(domain) # obtem o endereço do balanceador de carga a partir do domínio fornecido.

send_balance(address, message_connected) #enviam a mensagem de conexão para o balanceador de carga usando o endereço obtido