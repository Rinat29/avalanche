import psycopg2

# config
# bd_host = '172.16.117.193'
# bd_user = 'postgres'
# bd_password = '1234'
# db_name = 'testrinat'
# bd_port = '5432'

id = float(1)
k_st=float(0.00031)

try:
    connection = psycopg2.connect(
        host = '172.16.117.193',
        user = 'postgres',
        password = '1234',
        database = 'testrinat',
        port = '5432'
    )

    with connection.cursor() as cursor:
        cursor.execute ("SELECT * FROM in_tomorrowapidata ORDER BY temperature DESC;")
        rows = cursor.fetchone()
    windspeed = rows[3]
    winddirection = rows[4]
    # print ('[INFO]', 'windspeed = ', windspeed, 'winddirection = ', winddirection)    

    snow_transfer = k_st*windspeed**3
    print ('[INFO]', 'snow_transfer = ', snow_transfer)

    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO avalanche_problem (id, snow_transfer)
            VALUES (%s, %s);
            """,
            (id, float(snow_transfer)))
        connection.commit()
        print ("[INFO] Data was succefully inserted")

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        connection.close()
        print ("[INFO] PostgreSQL connection closed")
