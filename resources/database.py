import mysql.connector as mariadb

mariadb_connection = mariadb.connect(user="freecad", password="freecad", database="dbpezzi")
cursor = mariadb_connection.cursor()

cursor.execute("CREATE TABLE roasts (id INTEGER PRIMARY KEY, description TEXT NOT NULL UNIQUE, color TEXT NOT NULL UNIQUE);")