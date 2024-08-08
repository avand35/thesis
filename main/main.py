import psycopg2
from config import config


def connect():
    connection = None
    try: 
        params = config()
        print('Connecting to postgreSQL database ...')
        connection = psycopg2.connect(**params)


        # create a cursor
        cur = connection.cursor()
        print('PostgreSQL database version: ')
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)   
    except(Exception, psycopg2.DatabaseError)  as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database conenction terminated.')
if __name__ == "__main__":
    connect()
