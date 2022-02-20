#!/usr/bin/python
import psycopg2
from config import config


class Database:
    conn = None
    cursor = None

    def crea_tabella_parti(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS parti ("
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
        
    def inserisci_riga_parti(self, dati):
        campi_tubo = ("INSERT INTO parti "
                      "(riferimento, codice_padre, macchina, materiale, denominazione_profilo, data_creazione, ultima_modifica, nome, codice, cliente, quantità_per_disegno, misura_di_massima, massa, percorso) "
                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")

        self.cursor.execute(campi_tubo, dati)
        self.conn.commit()

    def verifica_tabelle_database(self):
        self.cursor.execute("SELECT * "
                       "FROM pg_catalog.pg_tables "
                       "WHERE schemaname != 'pg_catalog' AND "
                       "schemaname != 'information_schema' AND "
                       "tablename = 'parti';")
        tabella = self.cursor.fetchone()
        #print(tabella)
        if not tabella:
            self.crea_tabella_parti()

    def connect(self):
        """ Connect to the PostgreSQL database server """
        try:
            # read connection parameters
            params = config()

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(**params)

            # create a cursor
            self.cursor = self.conn.cursor()
            
            self.verifica_tabelle_database()
            
            dati_2 = ['primo', 'secondo', '', '', '', '2010-01-02 05:06:07', '2015-01-02 05:06:07', '', '', '', '5', '555', '6', 'questo percorso']
            
            self.inserisci_riga_parti(dati_2)
            
            self.cursor.close()
            self.conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()
                print('Database connection closed.')

if __name__ == '__main__':
    datab = Database()
    datab.connect()
    
