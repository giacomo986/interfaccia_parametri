import os
import json
import mysql.connector as mariadb


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
    cursor.execute("CREATE TABLE IF NOT EXISTS parti ("
                   "   parte_id INT AUTO_INCREMENT PRIMARY KEY,"
                   "   riferimento TEXT NOT NULL,"
                   "   codice_padre TEXT NOT NULL,"
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


def inserisci_riga_parti(dati):
    campi_tubo = ("INSERT INTO parti "
                  "(riferimento, codice_padre, macchina, materiale, denominazione_profilo, data_creazione, ultima_modifica, nome, codice, cliente, quantità_per_disegno, misura_di_massima, massa, percorso) "
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")

    cursor.execute(campi_tubo, dati)
    mariadb_connection.commit()


def aggiorna_riga_parti(dati):  # To Do: Finire query update
    query = ("UPDATE parti SET "
             f"codice_padre = '{dati[1]}', "
             f"macchina = '{dati[2]}', "
             f"materiale = '{dati[3]}', "
             f"denominazione_profilo = '{dati[4]}', "
             f"data_creazione = '{dati[5]}', "
             f"ultima_modifica = '{dati[6]}', "
             f"nome = '{dati[7]}', "
             f"codice = '{dati[8]}', "
             f"cliente = '{dati[9]}', "
             f"quantità_per_disegno = '{dati[10]}', "
             f"misura_di_massima = '{dati[11]}', "
             f"massa = '{dati[12]}' "
             #f"percorso = '{dati[13]}'"
             f"WHERE riferimento = '{dati[0]}';")

    cursor.execute(query)
    mariadb_connection.commit()
    return True


def verifica_tabelle_database():
    cursor.execute("SHOW TABLES LIKE 'parti';")
    tabella = cursor.fetchone()
    if not tabella:
        crea_tabella_parti()


def trova_id_parte(condizione):
    query = ("SELECT parte_id "
             f"FROM parti WHERE riferimento = '{condizione}';")
    #print("query = %s" % query)
    cursor.execute(query)
    tabella = cursor.fetchall()
    return tabella


def interroga_tabella_parti(condizioni):
    query = ("SELECT "
             "p.riferimento, "
             "p.codice_padre, "
             "p.macchina, "
             "p.materiale, "
             "p.denominazione_profilo, "
             "p.data_creazione, "
             "p.ultima_modifica, "
             "p.nome, "
             "p.codice, "
             "p.cliente, "
             "p.quantità_per_disegno, "
             "p.misura_di_massima, "
             "p.massa, "
             "p.percorso "
             "FROM parti p ")

    # controlla se il dizionario contiene dati per filtrare la query
    if condizioni:
        # inizializzazione variabili
        contatore = 0
        stringa = ""
        for i in condizioni:  # Per ogni campo (colonna del db) del dizionario
            # Per ogni condizione all'interno del campo (Per es: nome uguale a "xxx", massa minore di "yyy")
            for j in condizioni[i]:
                if j[0]:  # se esiste un valore di confronto diverso da ""
                    if contatore > 0:
                        stringa = f"{stringa} AND "
                    # aggiunge la condizione con i = nome della colonna, j[1] = operazione da copiere (es: "<=", "LIKE"), j[0] = valore di confronto
                    stringa = stringa + f"{i} {j[1]} '{j[0]}' "
                    contatore += 1
        if contatore > 0:
            query = f"{query} WHERE {stringa}"

    query = query + ";"
    #print("query = %s" % query)
    cursor.execute(query)
    tabella = cursor.fetchall()
    return tabella
