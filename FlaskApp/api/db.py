import psycopg2 as pdb
import psycopg2.extras
import sys

try:
    con = pdb.connect(database='ridemyway', user='postgres',\
                      password='6398litein', host="127.0.0.1", port="5432")
    con.autocommit=True
    cur = con.cursor()
    cur.execute('SELECT version()')
    var = cur.fetchone()

    print (var)
except Exception:
    print('not connected')

#CREATE A NEW TABLE

def create_table(con, query):
    with con:
        cur = con.cursor()
        cur.execute(query)
        con.commit()
# INSERT VALUES

def insertTable(con, query):
    with con:
        cur = con.cursor()

        cur.execute(query)
        con.commit()

def return_user(con, query):
    with con:
        cur = con.cursor()
        cur.execute(query)
        results = cur.fetchall()

        return results

def retrieveTable(con, query):
    with con:
        cur = con.cursor(cursor_factory=pdb.extras.DictCursor)
        cur.execute(query)
        rows = cur.fetchall()
        return rows

def drop_all(con):
    query1= 'DROP TABLE request CASCADE'
    cur.execute(query1)
    con.commit()

    query2= 'DROP TABLE rides CASCADE'
    cur.execute(query2)
    con.commit()

    query3= 'DROP TABLE users CASCADE'
    cur.execute(query3)
    con.commit()

    query4= 'DROP TABLE response CASCADE'
    cur.execute(query4)
    con.commit()