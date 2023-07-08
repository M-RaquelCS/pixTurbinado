import socket
import sqlite3

server_application = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_application.bind(('localhost', 3333))
server_application.listen()

connection, address = server_application.accept()
response = connection.recv(2048).decode()
print(response)

def login():
    connectionDB = sqlite3.connect('../database/db.db')
    cursor = connectionDB.cursor()

    command = "SELECT * FROM users"
    cursor.execute(command)
    result = cursor.fetchall()
    print(result)

# login()