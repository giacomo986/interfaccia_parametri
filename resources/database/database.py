import mysql.connector as mariadb


config = {
  'user': 'freecad',
  'password': 'freecad',
  'host': '127.0.0.1',
  'database': 'dbpezzi',
  'raise_on_warnings': True
}

def connetti():
  global mariadb_connection, cursor
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
                  "   misura_di_massima INT NOT NULL,"
                  "   massa INT NOT NULL"
                  ")  ENGINE=INNODB;")

def inserisci_riga(dati):
  campi_tubo = ("INSERT INTO tubi "
                "(riferimento, codice_padre, macchina, materiale, denominazione_profilo, data_creazione, nome, codice, cliente, quantità_per_disegno, misura_di_massima, massa)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

  cursor.execute(campi_tubo, dati)
  mariadb_connection.commit()

def verifica_tabella_database():
  tabella = cursor.execute("SHOW TABLES LIKE 'tubi';")
  tabella = cursor.fetchone()
  if not tabella:
    Crea_tabella()
# dati_tubo = ('a', 'b', 'c', 'd', 'e', '2019-12-10', 'g', 'h', '1', 'l', 'i', '5')