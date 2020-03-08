import mysql.connector as mariadb
import json

def connetti(cwd):
  global mariadb_connection, cursor

  with open(cwd + "/resources/database/db_config.json", "r") as read_file:
    config = json.load(read_file)
  try:
    mariadb_connection = mariadb.connect(**config)
    cursor = mariadb_connection.cursor(buffered=True)
    verifica_tabella_database()
    return True
  except:
    return False

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

def interroga_database(condizioni):
  query = ("SELECT "
          "riferimento, "
          "codice_padre, "
          "macchina, "
          "materiale, "
          "denominazione_profilo, "
          "data_creazione, "
          "nome, "
          "codice, "
          "cliente, "
          "quantità_per_disegno, "
          "misura_di_massima, "
          "massa, "
          "percorso "
          "FROM tubi ")

  if condizioni:
    query = query + "WHERE "
    for elemento in condizioni:
      if condizioni[elemento]:
        query = query + "%s = '%s' " % (elemento, condizioni[elemento])

  query = query + ";"
  print(query)
  cursor.execute(query)
  tabella = cursor.fetchall()
  return tabella

"SELECT article, dealer, price"
"FROM   shop"
"WHERE  price=(SELECT MAX(price) FROM shop);"