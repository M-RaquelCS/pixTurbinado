import sqlite3

def login():
    connectionDB = sqlite3.connect('../database/db.db')
    cursor = connectionDB.cursor()

    command = "SELECT * FROM users"
    cursor.execute(command)
    result = cursor.fetchall()
    print(result)

login()