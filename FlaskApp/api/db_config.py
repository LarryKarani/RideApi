import psycopg2 as pdb
import sys

# CREATE THE DATABASE


try:
    con = pdb.connect(database='ridemyway', user='postgres',\
                      password='6398litein', host="127.0.0.1", port="5432")
    con.autocommit=True
    cur = con.cursor()
    cur.execute('SELECT version()')
    var = cur.fetchone()

    print (var)

except Exception as e:
    print("Error %d: %s" % (e.args[0], e.args[1]))
    sys.exit(1)

