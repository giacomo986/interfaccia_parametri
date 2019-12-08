import mysql.connector as mariadb
#from config import config


config = {
  'user': 'freecad',
  'password': 'freecad',
  'host': '127.0.0.1',
  'database': 'dbpezzi',
  'raise_on_warnings': True
}

#mariadb_connection = mariadb.connect(   user="freecad",
#                                        password="freecad",
#                                        host="127.0.0.1", 
#                                        database="dbpezzi")
mariadb_connection = mariadb.connect(**config)

cursor = mariadb_connection.cursor()

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
                    "   quantità_per_disegno INT NOT NULL,"
                    "   misura_di_massima TEXT NOT NULL,"
                    "   massa INT NOT NULL"
                    ")  ENGINE=INNODB;")

def inserisci_riga():
    cursor.execute( "INSERT INTO tubi "
                    "(task_id, riferimento, codice_padre, macchina, materiale, denominazione_profilo, data_creazione, nome, codice, quantità_per_disegno, misura_di_massima, massa)"
                    "VALUES (%s, %s, %s, %s, %s)")

aggiungi_campi = (  "INSERT INTO tubi "
                    "(task_id, riferimento, codice_padre, macchina, materiale, denominazione_profilo, data_creazione, nome, codice, quantità_per_disegno, misura_di_massima, massa)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

dati_campi = ('1', 'a', 'b', 'c', 'd', 'e', '2019-12-10', 'g', 'h', '1', 'l', '5')

cursor.execute(aggiungi_campi, dati_campi)

#Crea_tabella()
#inserisci_riga()
mariadb_connection.commit()