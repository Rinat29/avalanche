import numpy
import psycopg2


connection = psycopg2.connect(
    database = 'testrinat',
    user="postgres",
    password = '1234',
    host = '172.16.117.193',
    port = '5432'
 )

cur = connection.cursor()
cur.execute("SELECT * FROM avalanche_problem ORDER BY id DESC;")
rows = cur.fetchone()
print (rows)