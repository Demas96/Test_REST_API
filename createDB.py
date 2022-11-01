import sqlite3
import conf

connection = sqlite3.connect(conf.PATH)
cursor = connection.cursor()
f = open('users.sql', 'r')
cursor.execute(f'{f.read()}')
connection.close()