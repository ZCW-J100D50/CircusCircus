import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Donald09",
)

my_cursor = mydb.cursor()

#my_cursor.execute("CREATE DATABASE circuscircus")
my_cursor.execute("DROP DATABASE circuscircus")
my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)
