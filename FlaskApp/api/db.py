import psycopg2 as pdb
import psycopg2.extras
import sys

try:
    con = pdb.connect(database='ridemyway', user='postgres',
                      password='6398litein', host="127.0.0.1", port="5432")
    con.autocommit = True
    cur = con.cursor()
    cur.execute('SELECT version()')
    var = cur.fetchone()

    print(var)
except Exception:
    print('not connected')

def create_table (con, query):
     
    with con:
        cur = con.cursor()
        cur.execute(query)
        con.commit()

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

    query1 = 'DROP TABLE IF EXISTS request CASCADE;'
    cur.execute(query1)
    query2 = 'DROP TABLE IF EXISTS rides CASCADE;'
    cur.execute(query2)
    query3 = ' DROP TABLE IF EXISTS usersCASCADE;'
    cur.execute(query3)
    query4 = 'DROP TABLE IF EXISTS response CASCADE;'
    cur.execute(query4)
    
