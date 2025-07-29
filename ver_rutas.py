import sqlite3

conn = sqlite3.connect("db/prueba.db")
print("¡Conexión exitosa!")
conn.close()