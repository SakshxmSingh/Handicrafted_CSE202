import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session
import os
import random
import string

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
            # print(user[0])
            session['user'] = user  # Store user ID in session
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
            session['admin'] = admin  # Store admin ID in session
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
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM employee")
        employees = cursor.fetchall()
        cursor.execute("SELECT * FROM product")
        products = cursor.fetchall()
        cursor.execute("SELECT * FROM category")
        categories = cursor.fetchall()
        cursor.execute("SELECT * FROM customer")
        customers = cursor.fetchall()
        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()
        cursor.execute("SELECT * FROM order_items")
        order_items = cursor.fetchall()
        cursor.close()
        return render_template('admin_dashboard.html', employees=employees, products=products, categories=categories, 
                               customers=customers, orders=orders, order_items=order_items)
    else:
        return redirect(url_for('index'))
    

@app.route('/admin_dashboard/add_employee', methods=['POST'])
def add_employee():
    if 'admin' in session:
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        passwd =  ''.join(random.choices(string.ascii_uppercase +string.digits, k=8))

        cursor = mydb.cursor()
        insert_query = "INSERT INTO employee (empname, phone_no, email, passwd) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (name, phone, email, passwd))
        mydb.commit()
        cursor.close()

        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('index'))
    
@app.route('/admin_dashboard/delete_employee/<int:employee_id>', methods=['GET'])
def delete_employee(employee_id):
    if 'admin' in session:
        cursor = mydb.cursor()
        delete_query = "DELETE FROM employee WHERE employee_id=%s"
        cursor.execute(delete_query, (employee_id,))
        mydb.commit()
        cursor.close()

        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('index'))
    
@app.route('/admin_dashboard/edit_data/employee/<int:employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    if 'admin' in session:
        if request.method == 'POST':
            name = request.form['empname']
            phone = request.form['phone_no']
            email = request.form['email']

            cursor = mydb.cursor()
            update_query = "UPDATE employee SET empname=%s, phone_no=%s, email=%s WHERE employee_id=%s"
            cursor.execute(update_query, (name, phone, email, employee_id))
            mydb.commit()
            cursor.close()

            return redirect(url_for('admin_dashboard'))
        else:
            cursor = mydb.cursor()
            select_query = "SELECT * FROM employee WHERE employee_id=%s"
            cursor.execute(select_query, (employee_id,))
            employee_data = cursor.fetchone()
            cursor.close()

            employee_dict = dict(zip([col[0] for col in cursor.description], employee_data))

            return render_template('edit_data.html', table_name='employee', data_id=employee_id, data=employee_dict)
    else:
        return redirect(url_for('index'))
    
@app.route('/admin_dashboard/add_product', methods=['POST'])
def add_product():
    if 'admin' in session:
        name = request.form['name']
        price = request.form['price']
        category_id = request.form['category']
        stock = request.form['stock']
        description = request.form['description']

        cursor = mydb.cursor()
        insert_query = "INSERT INTO product (productname, price, stockquantity, productdesc, category_ID) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (name, price, stock, description, category_id))
        mydb.commit()
        cursor.close()

        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('index'))
    
@app.route('/admin_dashboard/delete_product/<int:product_id>', methods=['GET'])
def delete_product(product_id):
    if 'admin' in session:
        cursor = mydb.cursor()
        delete_query = "DELETE FROM product WHERE product_ID=%s"
        cursor.execute(delete_query, (product_id,))
        mydb.commit()
        cursor.close()

        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('index'))

@app.route('/admin_dashboard/edit_data/product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if 'admin' in session:
        if request.method == 'POST':
            name = request.form['productname']
            price = request.form['price']
            category_id = request.form['category_ID']
            stock = request.form['stockquantity']
            description = request.form['productdesc']

            cursor = mydb.cursor()
            update_query = "UPDATE product SET productname=%s, price=%s, category_ID=%s, stockquantity=%s, productdesc=%s WHERE product_ID=%s"
            cursor.execute(update_query, (name, price, category_id, stock, description, product_id))
            mydb.commit()
            cursor.close()

            return redirect(url_for('admin_dashboard'))
        else:
            cursor = mydb.cursor()
            select_query = "SELECT * FROM product WHERE product_ID=%s"
            cursor.execute(select_query, (product_id,))
            product_data = cursor.fetchone()
            cursor.close()

            product_dict = dict(zip([col[0] for col in cursor.description], product_data))

            return render_template('edit_data.html', table_name='product', data_id=product_id, data=product_dict)
    else:
        return redirect(url_for('index'))
    
@app.route('/admin_dashboard/add_category', methods=['POST'])
def add_category():
    if 'admin' in session:
        name = request.form['name']
        description = request.form['description']

        cursor = mydb.cursor()
        insert_query = "INSERT INTO category (catname, catdesc) VALUES (%s, %s)"
        cursor.execute(insert_query, (name, description))
        mydb.commit()
        cursor.close()

        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('index'))
    
@app.route('/admin_dashboard/delete_category/<int:category_id>', methods=['GET'])
def delete_category(category_id):
    if 'admin' in session:
        cursor = mydb.cursor()
        delete_query = "DELETE FROM category WHERE category_ID=%s"
        cursor.execute(delete_query, (category_id,))
        mydb.commit()
        cursor.close()

        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('index'))

@app.route('/admin_dashboard/edit_data/category/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    if 'admin' in session:
        if request.method == 'POST':
            name = request.form['catname']
            description = request.form['catdesc']

            cursor = mydb.cursor()
            update_query = "UPDATE category SET catname=%s, catdesc=%s WHERE category_ID=%s"
            cursor.execute(update_query, (name, description, category_id))
            mydb.commit()
            cursor.close()

            return redirect(url_for('admin_dashboard'))
        else:
            cursor = mydb.cursor()
            select_query = "SELECT * FROM category WHERE category_ID=%s"
            cursor.execute(select_query, (category_id,))
            category_data = cursor.fetchone()
            cursor.close()

            category_dict = dict(zip([col[0] for col in cursor.description], category_data))

            return render_template('edit_data.html', table_name='category', data_id=category_id, data=category_dict)
    else:
        return redirect(url_for('index'))

@app.route('/admin_dashboard/delete_customer/<int:customer_ID>', methods=['GET'])
def delete_customer(customer_ID):
    if 'admin' in session:

        cursor = mydb.cursor()
        delete_query = "DELETE FROM customer WHERE customer_ID=%s"
        cursor.execute(delete_query, (customer_ID,))
        mydb.commit()
        cursor.close()

        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('index'))
    
@app.route('/admin_dashboard/delete_order/<int:order_ID>', methods=['GET'])
def delete_order(order_ID):
    if 'admin' in session:

        cursor = mydb.cursor()
        delete_query = "DELETE FROM orders WHERE order_ID=%s"
        cursor.execute(delete_query, (order_ID,))
        mydb.commit()
        cursor.close()

        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
