import sqlite3

conn = sqlite3.connect("../prueba.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tablas = cursor.fetchall()
print("Tablas en la base de datos:", tablas)

conn.close()
