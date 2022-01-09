#!/usr/bin/python
import psycopg2
from config import config

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
        cur = conn.cursor()
        
	# execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()
    
#docker run --name mariadbtest -e MYSQL_ROOT_PASSWORD=mypass -d -p 3306:3306  mariadb/server
#docker run --name freeprof -e POSTGRES_PASSWORD=freeprof -d postgres
#docker run --name freeprof -e POSTGRES_PASSWORD=esempio -d -p 5432:5432 postgres
#docker exec -ti freeprof psql -d postgres -U postgres
#CREATE USER freecad WITH PASSWORD 'freecad';
#CREATE DATABASE freeprof OWNER freecad;

#docker exec -ti freeprof psql -d freeprof -U freecad
#psql -h localhost -p 5432 -d freeprof -U freecad