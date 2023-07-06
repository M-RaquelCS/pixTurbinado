import sqlite3

connection = sqlite3.connect('db.db')

cursor = connection.cursor()

table_users_data = '''
  CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    agency INTEGER NOT NULL,
    account_number INTEGER NOT NULL,
    pix_key INTEGER NOT NULL,
    balance DECIMAL(10, 2),
    transactions_history TEXT
  )
'''

drop_table_users = '''
  DROP TABLE IF EXISTS users
'''

add_user = '''
  INSERT INTO users (name, agency, account_number, pix_key, balance) 
  VALUES (?, ?, ?, ?, ?)
'''
name = 'Thaymara'
agency =  7667
account_number = 8778
pix_key = 9102
balance = 50.00

cursor.execute(table_users_data)
cursor.execute(add_user, (name, agency, account_number, pix_key, balance))

table_history_all_transactions_data = '''
  CREATE TABLE IF NOT EXISTS history_all_transactions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_transaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    origin_transaction INTEGER NOT NULL,
    destination_transaction INTEGER NOT NULL,
    value_transaction DECIMAL(10, 2),
    FOREIGN KEY (origin_transaction) REFERENCES users(pix_key),
    FOREIGN KEY (destination_transaction) REFERENCES users(pix_key)
  )
'''
cursor.execute(table_history_all_transactions_data)


connection.commit()
connection.close()