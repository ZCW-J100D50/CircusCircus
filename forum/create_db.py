import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="chrism",
    passwd="lesson",
)

my_cursor = mydb.cursor()

my_cursor.execute("CREATE DATABASE circuscircus")
#my_cursor.execute("DROP DATABASE circuscircus")
my_cursor.execute("UPDATE TABLE ")
my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)
