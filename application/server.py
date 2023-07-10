import multiprocessing
import subprocess # para executar comandos do sistema operacional 

def run_dns():
    dns = "python ./application/dns.py"
    subprocess.run(dns, shell=True)

def run_loadBalancer():
    loadBalancer = "python ./application/loadBalancer.py"
    subprocess.run(loadBalancer, shell=True)

def run_edge():
    edge = "python ./application/edge.py"
    subprocess.run(edge, shell=True)

def run_server():
    server= "python ./application/server.py"
    subprocess.run(server, shell=True)

def run_client():
    client = "python ./application/cliente.py"
    subprocess.run(client, shell=True)

# garante que o código dentro dele só será executado se o script for executado diretamente,
# e não quando importado como um módulo.
if __name__ == '__main__':
    process_dns = multiprocessing.Process(target=run_dns)
    process_dns.start()

    process_loadBalancer = multiprocessing.Process(target=run_loadBalancer)
    process_loadBalancer.start()

    process_edge= multiprocessing.Process(target=run_edge)
    process_edge.start()

    process_edge2 = multiprocessing.Process(target=run_edge)
    process_edge2.start()

    process_server = multiprocessing.Process(target=run_server)
    process_server.start()



