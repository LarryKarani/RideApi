import psycopg2 as pdb
import sys, os

# CREATE THE DATABASE
db_name= os.getenv("DATABASE_NAME")

try:
    con = pdb.connect(database=db_name, user='postgres',\
                      password='6398litein', host="127.0.0.1", port="5432")
    con.autocommit=True
    cur = con.cursor()
    cur.execute('SELECT version()')
    var = cur.fetchone()

    print (var)

except Exception:
    print("not connected")