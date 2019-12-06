import mysql.connector as mariadb

mariadb_connection = mariadb.connect(user="freecad", password="freecad", database="dbpezzi")
cursor = mariadb_connection.cursor()

def Crea_tabella():
    cursor.execute( "CREATE TABLE IF NOT EXISTS tubi ("
                    "   task_id INT AUTO_INCREMENT PRIMARY KEY,"
                    "   riferimento VARCHAR(255) NOT NULL,"
                    "   codice_padre TEXT,"
                    "   macchina TEXT,"
                    "   materiale TEXT,"
                    "   denominazione_profilo TEXT,"
                    "   data_creazione DATE,"
                    "   nome TEXT,"
                    "   codice TEXT,"
                    "   quantità_per_disegno INT,"
                    "   misura_di_massima TEXT,"
                    "   massa INT,"
                    "   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
                    ")  ENGINE=INNODB;")

def inserisci_riga();
    pass