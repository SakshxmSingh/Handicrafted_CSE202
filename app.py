import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

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
    # cursor = mydb.cursor()
    # cursor.execute("SELECT * FROM admins")
    # data = cursor.fetchall()
    # cursor.close()
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['email']
    password = request.form['password']
    role = request.form['role']

    cursor = mydb.cursor()

    if role == 'user':
        query = "SELECT * FROM customer WHERE email = %s AND passwd = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        if user:
            print(user[0])
            session['user'] = user[0]  # Store user ID in session
            return redirect(url_for('user_dashboard'))
        else:
            error = 'Invalid credentials. Please try again.'
            return render_template('login.html', error=error)
    elif role == 'admin':
        query = "SELECT * FROM admins WHERE email = %s AND passwd = %s"
        cursor.execute(query, (username, password))
        admin = cursor.fetchone()
        if admin:
            print(admin[0])
            session['admin'] = admin[0]  # Store admin ID in session
            return redirect(url_for('admin_dashboard'))
        else:
            error = 'Invalid credentials. Please try again.'
            return render_template('login.html', error=error)

    cursor.close()

@app.route('/user_dashboard')
def user_dashboard():
    if 'user' in session:
        # Display user dashboard
        return render_template('user_dashboard.html')
    else:
        return redirect(url_for('index'))

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin' in session:
        # Display admin dashboard
        return render_template('admin_dashboard.html')
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
