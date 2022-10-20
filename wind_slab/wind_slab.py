import numpy
import psycopg2

connection = psycopg2.connect(
    database = 'weather_prod',
    user="postgres",
    password = 'root',
    host = '172.16.117.159',
    port = '5432'
 )

cur = connection.cursor()
cur.execute("SELECT * FROM in_tw_api ORDER BY id DESC;")
rows = cur.fetchone()
# print (rows)

windspeed = rows[4]
winddirection = rows[5]
# print('windspeed =  ', windspeed)
# print('winddirection =  ', winddirection)

# wind_s1 = float(8)
# wind_s6 = numpy.array([8,8,8,8,8,8])
# format_snow = int (1) # значения 1 - много снега доступно 0,5 - не много снега доступно для переноса 0,1 - почти нет снега для переноса
k_st = 0.00031

snow_t = (k_st*windspeed**3) #  суммарный перенос за 1 час

# snow_t6 = sum(wind_s6**3*k_st)

print ('snow_t = ', snow_t)
# print (snow_t6)
connection.close

connection = psycopg2.connect(
    database = 'testrinat',
    user="postgres",
    password = '1234',
    host = '172.16.117.193',
    port = '5432'
 )

cur.execute("INSERT INTO testrinat (id, snow_t) VALUES (%s, %s)")
