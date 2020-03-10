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
          "FROM tubi")

  # controlla se il dizionario contiene dati per filtrare la query
  if condizioni:
    # inizializzazione variabili
    contatore = 0
    stringa = ""

    for i in condizioni: # Per ogni campo (colonna del db) del dizionario
      for j in condizioni[i]: # Per ogni condizione all'interno del campo (Per es: nome uguale a "xxx", massa minore di "yyy")
        if j[0]: # se esiste un valore di confronto diverso da ""
          if contatore > 0:
            stringa = stringa + "AND "
          stringa = stringa + "%s %s '%s' " % (i, j[1], j[0]) # aggiunge la condizione con i = nome della colonna, j[1] = operazione da copiere (es: "<="), j[0] = valore di confronto
    if contatore > 0:
      query = query + " WHERE " + stringa

  query = query + ";"
  #print(query)
  cursor.execute(query)
  tabella = cursor.fetchall()
  return tabella



'''
  if condizioni:
    contatore = 0
    cond = ""
    for elemento in condizioni:
      if condizioni[elemento]:
        if contatore > 0:
          stringa = stringa + "AND "
        stringa = stringa + "%s = '%s' " % (elemento, condizioni[elemento])
        contatore += 1
    if contatore > 0:
      query = query + " WHERE " + stringa'''