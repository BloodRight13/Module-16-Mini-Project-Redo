import os
import psycopg2

def get_db_connection():
    try:
      conn = psycopg2.connect(
        host=os.environ['RENDER_DB_HOST'],
        database=os.environ['RENDER_DB_NAME'],
        user=os.environ['RENDER_DB_USER'],
        password=os.environ['RENDER_DB_PASSWORD'],
        port=os.environ['RENDER_DB_PORT']
      )
      return conn
    except Exception as e:
      print(f"Error connecting to the database {e}")
      return None