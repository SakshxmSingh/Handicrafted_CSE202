import mysql.connector

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="12345678",
    database="handicrafted"
)

if mydb.is_connected():
    print("Connection Successful")
