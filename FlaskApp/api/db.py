import psycopg2 as pdb
import psycopg2.extras
from .db_config import con
import sys



def create_table():
     
        with con:
            query1='CREATE TABLE IF NOT EXISTS users (Id SERIAL PRIMARY KEY, username VARCHAR(255),\
                        password VARCHAR(255), email VARCHAR(255));'

            query2='CREATE TABLE IF NOT EXISTS rides(Id SERIAL PRIMARY KEY, current_location VARCHAR(255),\
                     destination VARCHAR(255), depature_time VARCHAR(255), seats_available VARCHAR(255),\
                     user_id SERIAL, FOREIGN KEY (user_id) REFERENCES users(Id), cost INTEGER);'

            query3= 'CREATE TABLE IF NOT EXISTS request(Id SERIAL PRIMARY KEY, Username VARCHAR(255),\
                      current_location VARCHAR(255), destination VARCHAR(255) , depature_time VARCHAR(255),\
                      request_id SERIAL, FOREIGN KEY(request_id) REFERENCES rides (Id));'

            query4='CREATE TABLE IF NOT EXISTS response(Id SERIAL PRIMARY KEY,\
                request_id SERIAL, rideoffer_id SERIAL, user_id SERIAL, reply VARCHAR(255),\
                FOREIGN KEY(rideoffer_id) REFERENCES rides (Id),\
                        FOREIGN KEY(request_id) REFERENCES request (Id),\
                        FOREIGN KEY(user_id) REFERENCES users(Id));'

            cur = con.cursor()
            cur.execute(query1)
            cur.execute(query2)
            cur.execute(query3)
            cur.execute(query4)
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
    cur=con.cursor()
    query1 = 'DROP TABLE IF EXISTS request CASCADE;'
    cur.execute(query1)
    query2 = 'DROP TABLE IF EXISTS rides CASCADE;'
    cur.execute(query2)
    query3 = ' DROP TABLE IF EXISTS usersCASCADE;'
    cur.execute(query3)
    query4 = 'DROP TABLE IF EXISTS response CASCADE;'
    cur.execute(query4)
    