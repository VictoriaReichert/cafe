# более легкий способ
import mysql.connector

cnx = mysql.connector.connect(user='root', password='p',
                              host='127.0.0.1',
                              database='cafe')

cursor = cafe_db.cursor()
select_query = "SELECT * FROM coffee"
cursor.execute(select_query)
results = cursor.fetchall()
print(results)

# with cafe_db.cursor() as cursor:
#     result = cursor.execute("SELECT * FROM coffee")
#     rows = cursor.fetchall()
#
#     for row in rows:
#         print(row)


cafe_db.close()
