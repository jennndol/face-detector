import sqlite3

connection = sqlite3.connect('database.db')
sqlite = connection.cursor()

query = """
DROP TABLE IF EXISTS users;
CREATE TABLE users (
           id integer unique primary key autoincrement,
           name text
);
"""
sqlite.executescript(query)
connection.commit()
connection.close()