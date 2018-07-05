import psycopg2 as pdb

import os

db_name = os.getenv("DATABASE_NAME")

con = pdb.connect(database=db_name, user='postgres',
                         password='6398litein', host="127.0.0.1", port="5432")
con.autocommit = True
