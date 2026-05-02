import psycopg2

def connect():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="0710" 
    )
    return conn
