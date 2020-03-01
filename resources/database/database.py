import mysql.connector as mariadb
import json

def connetti(cwd):
  global mariadb_connection, cursor

  with open(cwd + "/resources/database/db_config.json", "r") as read_file:
    config = json.load(read_file)

  mariadb_connection = mariadb.connect(**config)
  cursor = mariadb_connection.cursor(buffered=True)
  verifica_tabella_database()

def disconnetti():
  cursor.close()
  mariadb_connection.close()

def Crea_tabella():
  cursor.execute( "CREATE TABLE IF NOT EXISTS tubi ("
                  "   task_id INT AUTO_INCREMENT PRIMARY KEY,"
                  "   riferimento TEXT NOT NULL,"
                  "   codice_padre TEXT NOT NULL,"
                  "   macchina TEXT NOT NULL,"
                  "   materiale TEXT NOT NULL,"
                  "   denominazione_profilo TEXT NOT NULL,"
                  "   data_creazione DATETIME NOT NULL,"
                  "   nome TEXT NOT NULL,"
                  "   codice TEXT NOT NULL,"
                  "   cliente TEXT NOT NULL,"
                  "   quantità_per_disegno INT NOT NULL,"
                  "   misura_di_massima FLOAT NOT NULL,"
                  "   massa FLOAT NOT NULL,"
                  "   percorso TEXT NOT NULL"
                  ")  ENGINE=INNODB;")

def inserisci_riga(dati):
  campi_tubo = ("INSERT INTO tubi "
                "(riferimento, codice_padre, macchina, materiale, denominazione_profilo, data_creazione, nome, codice, cliente, quantità_per_disegno, misura_di_massima, massa, percorso)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

  cursor.execute(campi_tubo, dati)
  mariadb_connection.commit()

def verifica_tabella_database():
  cursor.execute("SHOW TABLES LIKE 'tubi';")
  tabella = cursor.fetchone()
  if not tabella:
    Crea_tabella()

def interroga_database():
  cursor.execute("SELECT * FROM tubi;")
  risultati = cursor.fetchall()
  for x in risultati:
    print(x)
    print(x[13])
  return risultati