import psycopg2
from config import db_host, db_user, db_password, db_name, db_port

id = float(1)
k_st=float(0.00031)

try:
    connection = psycopg2.connect( # подключение к базе данных
        host = db_host,
        user = db_user,
        password = db_password,
        database = db_name,
        port = db_port
    )

    with connection.cursor() as cursor:  # забираем строку с низу из таблицы in_tw_data
        cursor.execute ("SELECT * FROM in_tw_data ORDER BY temperature DESC;")
        rows = cursor.fetchone()
        windspeed = rows[3]
        winddirection = rows[4]
        print ('[INFO]', 'windspeed = ', windspeed, 'winddirection = ', winddirection)    

    snow_transfer = k_st*windspeed**3 # расчитываем количество перенесенного снега
    print ('[INFO]', 'snow_transfer = ', snow_transfer)

    if snow_transfer >= 2:      # вычисляем значение wind_slab
        wind_slab = 1
    elif snow_transfer >= 1 :
        wind_slab = 0.66
    elif snow_transfer >= 0.5 :
        wind_slab = 0.33
    else:
        wind_slab = 0

    with connection.cursor() as cursor: # записываем полученное значение в таблицу avalanche_problem
        cursor.execute("""
            INSERT INTO avalanche_problem (id, snow_transfer, wind_slab) 
            VALUES (%s, %s, %s);
            """,
            (id, float(snow_transfer), float(wind_slab))
            )
        connection.commit()
        print ("[INFO] Data was succefully inserted")

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        connection.close()
        print ("[INFO] PostgreSQL connection closed")
