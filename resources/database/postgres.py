#!/usr/bin/python
import psycopg2
from config import config

def crea_tabella_parti(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS parti ("
                    "parte_id                serial PRIMARY KEY, "
                    "riferimento             TEXT NOT NULL, "
                    "codice_padre            TEXT NOT NULL, "
                    "macchina                TEXT NOT NULL, "
                    "materiale               TEXT NOT NULL, "
                    "denominazione_profilo   TEXT NOT NULL, "
                    "data_creazione          date NOT NULL, "
                    "ultima_modifica         date NOT NULL, "
                    "nome                    TEXT NOT NULL, "
                    "codice                  TEXT NOT NULL, "
                    "cliente                 TEXT NOT NULL, "
                    "quantità_per_disegno    INT NOT NULL, "
                    "misura_di_massima       FLOAT NOT NULL, "
                    "massa                   FLOAT NOT NULL, "
                    "percorso                TEXT NOT NULL "
                    ");")
    
def inserisci_riga_parti(conn, cursor, dati):
    campi_tubo = ("INSERT INTO parti "
                  "(riferimento, codice_padre, macchina, materiale, denominazione_profilo, data_creazione, ultima_modifica, nome, codice, cliente, quantità_per_disegno, misura_di_massima, massa, percorso) "
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")

    cursor.execute(campi_tubo, dati)
    conn.commit()

def verifica_tabelle_database(cursor):
    cursor.execute("SELECT * "
                   "FROM pg_catalog.pg_tables "
                   "WHERE schemaname != 'pg_catalog' AND "
                   "schemaname != 'information_schema' AND "
                   "tablename = 'parti';")
    tabella = cursor.fetchone()
    #print(tabella)
    if not tabella:
        crea_tabella_parti(cursor)

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cursor = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cursor.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cursor.fetchone()
        print(db_version)

        verifica_tabelle_database(cursor)
        """
        cursor.execute("CREATE TABLE IF NOT EXISTS parti ("
                    "parte_id                serial PRIMARY KEY, "
                    "riferimento             TEXT NOT NULL, "
                    "codice_padre            TEXT NOT NULL, "
                    "macchina                TEXT NOT NULL, "
                    "materiale               TEXT NOT NULL, "
                    "denominazione_profilo   TEXT NOT NULL, "
                    "data_creazione          date NOT NULL, "
                    "ultima_modifica         date NOT NULL, "
                    "nome                    TEXT NOT NULL, "
                    "codice                  TEXT NOT NULL, "
                    "cliente                 TEXT NOT NULL, "
                    "quantità_per_disegno    INT NOT NULL, "
                    "misura_di_massima       FLOAT NOT NULL, "
                    "massa                   FLOAT NOT NULL, "
                    "percorso                TEXT NOT NULL "
                    ");")
        """
        dati_2 = ['primo', 'secondo', '', '', '', '2010-01-02 05:06:07', '2015-01-02 05:06:07', '', '', '', '5', '555', '6', 'questo percorso']
        
        inserisci_riga_parti(conn, cursor, dati_2)
        
        cursor.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()
