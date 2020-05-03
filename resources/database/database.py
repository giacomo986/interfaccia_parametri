import subprocess, os, json

try:
  import mysql.connector as mariadb
except:
  print("modulo mysql connector non trovato, provo a scaricarlo.")
  if os.name == "nt": # se la macro viene lanciata in ambiente windows
    subprocess.call([os.getcwd() + "//python", "-m", 'pip', 'install', "mysql-connector-python"], shell=True)
  else: # altrimenti siamo su linux
    try:
      subprocess.call([sys.executable, "-m", 'pip', 'install', "mysql-connector-python"], shell=True) # comando completo per l'installazione nella versione di python corretta
    except:
      subprocess.call(['pip', 'install', "mysql-connector-python"], shell=True) # comando che funziona nell'Appimage
finally:
  import mysql.connector as mariadb
  print("modulo mysql trovato")

def connetti(cwd):
  global mariadb_connection, cursor

  with open(cwd + "/resources/database/db_config.json", "r") as read_file:
    config = json.load(read_file)
  try:
    mariadb_connection = mariadb.connect(**config)
    cursor = mariadb_connection.cursor(buffered=True)
  except:
    return False

  verifica_tabelle_database()
  return True

def disconnetti():
  cursor.close()
  mariadb_connection.close()

def crea_tabella_parti():
  cursor.execute( "CREATE TABLE IF NOT EXISTS parti ("
                  "   parte_id INT AUTO_INCREMENT PRIMARY KEY,"
                  "   riferimento TEXT NOT NULL,"
                  "   id_codice_padre INT NOT NULL,"
                  "   INDEX (id_codice_padre),"
                  "   FOREIGN KEY (id_codice_padre) REFERENCES assiemi(assieme_id),"
                  "   macchina TEXT NOT NULL,"
                  "   materiale TEXT NOT NULL,"
                  "   denominazione_profilo TEXT NOT NULL,"
                  "   data_creazione DATETIME NOT NULL,"
                  "   ultima_modifica DATETIME NOT NULL,"
                  "   nome TEXT NOT NULL,"
                  "   codice TEXT NOT NULL,"
                  "   cliente TEXT NOT NULL,"
                  "   quantità_per_disegno INT NOT NULL,"
                  "   misura_di_massima FLOAT NOT NULL,"
                  "   massa FLOAT NOT NULL,"
                  "   percorso TEXT NOT NULL"
                  ")  ENGINE=INNODB;")

def crea_tabella_assiemi():
  cursor.execute( "CREATE TABLE IF NOT EXISTS assiemi ("
                  "   assieme_id INT AUTO_INCREMENT, PRIMARY KEY (assieme_id),"
                  "   codice_padre TEXT NOT NULL,"
                  "   macchina TEXT NOT NULL,"
                  "   data_creazione DATETIME NOT NULL,"
                  "   ultima_modifica DATETIME NOT NULL,"
                  "   cliente TEXT NOT NULL,"
                  "   percorso TEXT NOT NULL"
                  ")  ENGINE=INNODB;")

def inserisci_riga_assiemi(dati):
  campi_assieme = ("INSERT INTO assiemi "
                "(codice_padre, macchina, data_creazione, ultima_modifica, cliente, percorso)"
                "VALUES (%s, %s, %s, %s, %s, %s);")
  
  cursor.execute(campi_assieme, dati)
  mariadb_connection.commit()

def inserisci_riga_parti(dati):
  campi_tubo = ("INSERT INTO parti "
                "(riferimento, id_codice_padre, macchina, materiale, denominazione_profilo, data_creazione, ultima_modifica, nome, codice, cliente, quantità_per_disegno, misura_di_massima, massa, percorso) "
                "VALUES (%s, (SELECT assieme_id FROM assiemi WHERE codice_padre = %s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")

  cursor.execute(campi_tubo, dati)
  mariadb_connection.commit()

def aggiorna_riga_parti(dati): # To Do: Finire query update 
  campi_tubo = ("UPDATE parti SET " 
                "id_codice_padre = %s, " % dati[1] +
                "macchina = %s, " % dati[2] +
                "materiale = %s, " % dati[3] +
                "denominazione_profilo = %s, " % dati[4] +
                "data_creazione = %s, " % dati[5] +
                "ultima_modifica = %s, " % dati[6] +
                "nome = %s, " % dati[7] +
                "codice = %s, " % dati[8] +
                "cliente = %s, " % dati[9] +
                "quantità_per_disegno = %s, " % dati[10] +
                "misura_di_massima = %s, " % dati[11] +
                "massa = %s, " % dati[12] +
                "percorso = %s" % dati[13] +
                "WHERE riferimento = %s;" % dati[0])
  
  cursor.execute(campi_tubo, dati)
  mariadb_connection.commit()

def verifica_tabelle_database():
  cursor.execute("SHOW TABLES LIKE 'assiemi';")
  tabella = cursor.fetchone()
  if not tabella:
    crea_tabella_assiemi()

  cursor.execute("SHOW TABLES LIKE 'parti';")
  tabella = cursor.fetchone()
  if not tabella:
    crea_tabella_parti()

def trova_id_parte(condizione):
  query = ("SELECT parte_id "
          "FROM parti WHERE riferimento = '%s';" % condizione)
  #print("query = %s" % query)
  cursor.execute(query)
  tabella = cursor.fetchall()
  return tabella

def trova_id_assieme(condizione):
  query = ("SELECT assieme_id "
          "FROM assiemi WHERE codice_padre = '%s';" % condizione)
  #print("query = %s" % query)
  cursor.execute(query)
  tabella = cursor.fetchall()
  return tabella

def interroga_tabella_parti(condizioni):
  query = ("SELECT "
          "p.riferimento, "
          "a.codice_padre, "
          "p.macchina, "
          "p.materiale, "
          "p.denominazione_profilo, "
          "p.data_creazione, "
          "p.nome, "
          "p.codice, "
          "p.cliente, "
          "p.quantità_per_disegno, "
          "p.misura_di_massima, "
          "p.massa, "
          "p.percorso "
          "FROM parti p inner join assiemi a on p.id_codice_padre = a.assieme_id ")

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
          stringa = stringa + "%s %s '%s' " % (i, j[1], j[0]) # aggiunge la condizione con i = nome della colonna, j[1] = operazione da copiere (es: "<=", "LIKE"), j[0] = valore di confronto
          contatore += 1
    if contatore > 0:
      query = query + " WHERE " + stringa

  query = query + ";"
  #print("query = %s" % query)
  cursor.execute(query)
  tabella = cursor.fetchall()
  return tabella