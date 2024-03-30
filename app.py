import mysql.connector
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="12345678",
    database="handicrafted"
)

# if mydb.is_connected():
#     print("Connection Successful")

@app.route('/')
def index():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM admins")
    data = cursor.fetchall()
    cursor.close()
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
