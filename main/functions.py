import psycopg2
import os
import sys
import pandas as pd
from psycopg2 import sql, Error
from dotenv import load_dotenv

load_dotenv(dotenv_path='/Users/avanedaei/Desktop/thesis/main/thesis/touch.env')

def connect():

   conn = None
   try:
      print("Connecting…")
      conn = psycopg2.connect(
                   database=os.environ["DB_NAME"],
                   user=os.environ["DB_USER"],
                   password=os.environ["DB_PASSWORD"],
                   host=os.environ["DB_HOST"],
                   port=os.environ["DB_PORT"])
   except (Exception, psycopg2.DatabaseError) as error:
       print(error)
       sys.exit(1)
   print("All good, Connection successful!")
   return conn

def sql_to_dataframe(conn, query, column_names):
   """ 
   Import data from a PostgreSQL database using a SELECT query 
   """
   try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            tuples_list = cursor.fetchall()
            df = pd.DataFrame(tuples_list, columns=column_names)
            return df
   except (Exception, psycopg2.DatabaseError) as error:
        print('Error: %s' % error)
        return pd.DataFrame()  # Return an empty DataFrame on error

# Function to fetch column names for a given table
def fetch_column_names(conn, table_name):
    try:
        query = sql.SQL("SELECT column_name FROM information_schema.columns WHERE table_name = %s")
    
        with conn.cursor() as cur:
                cur.execute(query, (table_name,))
                columns = [row[0] for row in cur.fetchall()]
                return columns
    except Error as e:
        print(f"Error fetching column names: {e}")
        conn.rollback()  # Rollback transaction
        return []