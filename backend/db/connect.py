# более легкий способ
import mysql.connector

cnx = mysql.connector.connect(user='root', password='p',
                              host='127.0.0.1',
                              database='cafe')

with cnx.cursor() as cursor:
    result = cursor.execute("SELECT * FROM coffee")
    rows = cursor.fetchall()

    for rows in rows:
        print(rows)


cnx.close()
