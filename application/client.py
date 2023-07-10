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
  # print("Conectado ao Balanceador")

  balancer_socket.send(request.encode()) # envio da mensagem de resquisição (a primeira é um aviso de que o client está conectado)

  response = balancer_socket.recv(1024).decode() # recebo uma resposta vinda do balanceador sobre minha requisição
  balancer_socket.close()
  return response

domain = input("Escreva seu domínio: ")

# messagem para "avisar" que o client está conectado
message_connected = message_constructor.message(5, process_id, 0, 0, 0)
address = get_address(domain)

response = send_balance(address, message_connected)

if response:
  if response.split('|')[0] == '6':
    process_id = response.split('|')[1]

    print('bem-vindos ao pix\n'
        'Digite sua agência:')
    agency = input("->")

    print("Digite a sua conta:")
    account_number = input("-> ")

    if (agency, account_number):
      message_login = message_constructor.message(6, process_id, agency, account_number, 0)
      response = send_balance(address, message_login)

      if response.split('|')[0] == '6' and response.split('|')[2] != '0000':
        print('Para fazer o pix, por favor digite a conta destino:')
        destiny_account = input("-> ")

        print('e o valor da transação:')
        value_transaction = input("-> ")
        
        if (destiny_account, value_transaction):
          message_transaction = message_constructor.message(3, process_id, account_number, destiny_account, value_transaction)
          response = send_balance(address, message_transaction)



