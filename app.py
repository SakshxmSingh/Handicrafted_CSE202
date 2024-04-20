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
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['email']
    password = request.form['password']
    role = request.form['role']

    cursor = mydb.cursor()
    mydb.commit()

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
            # print(admin[0])
            session['admin'] = admin  # Store admin ID in session
            return redirect(url_for('admin_dashboard'))
        else:
            error = 'Invalid credentials. Please try again.'
            return render_template('login.html', error=error)

    cursor.close()

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register/create_user', methods=['POST'])
def register_user():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    address = request.form['address']
    password = request.form['password']

    cursor = mydb.cursor()
    mydb.commit()
    insert_query = "INSERT INTO customer (fullname, phone_no, email, address, passwd) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (name, phone, email, address, password))
    # get the last row id
    customer_ID = cursor.lastrowid
    cart_inset_query = "INSERT INTO cart (customer_ID) VALUES (%s)"
    cursor.execute(cart_inset_query, (customer_ID,))
    mydb.commit()
    cursor.close()

    return render_template('login.html', success='Registration successful. Please login to continue.')

def calculate_cart_total(cart_items, products):
    cart_total = 0
    for item in cart_items:
        product_ID = item[1]
        quantity = item[2]
        product_price = products[product_ID - 1][2]
        item_total = product_price * quantity
        cart_total += item_total
    return cart_total

@app.route('/user_dashboard')
def user_dashboard():
    if 'user' in session:
        # Display user dashboard

        cursor = mydb.cursor()
        mydb.commit()
        cursor.execute("SELECT * FROM product")
        products = cursor.fetchall()
        cursor.execute("SELECT * FROM category")
        categories = cursor.fetchall()
        cursor.execute("SELECT * FROM orders WHERE customer_ID=%s", (session['user'][0],))
        user_orders = cursor.fetchall()
        cursor.execute("SELECT * FROM order_items")
        order_items = cursor.fetchall()
        cursor.execute("SELECT * FROM cart_items WHERE cart_ID=%s", (session['user'][0],))
        cart_items = cursor.fetchall()
        cursor.close()
        return render_template('user_dashboard.html', products=products, categories=categories, 
                               orders=user_orders, order_items=order_items, cart_items=cart_items, 
                               cart_total=calculate_cart_total(cart_items, products)
                               )
    else:
        return redirect(url_for('index'))
        
@app.route('/user_dashboard/product_search', methods=['POST'])
def product_search():
    if 'user' in session:
        search_query = request.form['search']
        category_filter = request.form['category']
        price_filter = request.form['price']
        stock_filter = request.form['stock']

        cursor = mydb.cursor()
        search_query = "%" + search_query + "%"  # Add wildcard characters for partial matching

        filters = []

        if category_filter != 'all':
            filters.append(f"c.category_ID = '{category_filter}'")

        if price_filter == 'low':
            filters.append("price ORDER BY price ASC")
        elif price_filter == 'high':
            filters.append("price ORDER BY price DESC")

        if stock_filter == 'in_stock':
            filters.append("stockquantity > 0")
        elif stock_filter == 'out_of_stock':
            filters.append("stockquantity = 0")

        if search_query:
            query = "SELECT p.* FROM product p JOIN category c ON p.category_ID = c.category_ID WHERE (p.productname LIKE %s OR c.catname LIKE %s)"
        else:
            query = "SELECT * FROM product p JOIN category c ON p.category_ID = c.category_ID"
        
        if filters:
            query += " AND " + " AND ".join(filters)

        cursor.execute(query, (search_query, search_query))
        search_results = cursor.fetchall()

        cursor.execute("SELECT * FROM category")
        categories = cursor.fetchall()
        cursor.execute("SELECT * FROM orders WHERE customer_ID=%s", (session['user'][0],))
        user_orders = cursor.fetchall()
        cursor.execute("SELECT * FROM order_items")
        order_items = cursor.fetchall()
        cursor.execute("SELECT * FROM cart_items WHERE cart_ID=%s", (session['user'][0],))
        cart_items = cursor.fetchall()
        cursor.execute("SELECT * FROM product")
        products = cursor.fetchall()
        cursor.close()

        return render_template('user_dashboard.html', products=products, search_results=search_results,  categories=categories, 
                                search_query=search_query,
                                orders=user_orders, order_items=order_items, cart_items=cart_items, 
                                cart_total=calculate_cart_total(cart_items, products))
    else:
        return redirect(url_for('index'))

@app.route('/user_dashboard/add_to_cart/<int:product_ID>', methods=['POST'])
def add_to_cart(product_ID):
    if 'user' in session:
        quantity = request.form['quantity']

        action = request.form['action']
        if action == 'add_to_cart':
            cursor = mydb.cursor()
            cursor.execute("SELECT stockquantity FROM product WHERE product_ID=%s", (product_ID,))
            stock = cursor.fetchone()[0]
            if int(quantity) > stock:
                error = 'Quantity exceeds stock limit. Please try again.'
                return render_template('user_dashboard.html', error=error)
            cursor.execute("SELECT * FROM cart_items WHERE product_ID=%s AND cart_ID=%s", (product_ID, session['user'][0]))
            item = cursor.fetchone()

            if item:
                cursor.execute("SELECT quantity FROM cart_items WHERE product_ID=%s AND cart_ID=%s", (product_ID, session['user'][0]))
                current_quantity = cursor.fetchone()[0]
                quantity = int(quantity) + current_quantity
                update_query = "UPDATE cart_items SET quantity=%s WHERE product_ID=%s AND cart_ID=%s"
                cursor.execute(update_query, (quantity, product_ID, session['user'][0]))
            else:
                insert_query = "INSERT INTO cart_items (product_ID, cart_ID, quantity) VALUES (%s, %s, %s)"
                cursor.execute(insert_query, (product_ID, session['user'][0], quantity))

            mydb.commit()
            cursor.execute("SELECT * FROM product")
            products = cursor.fetchall()
            cursor.execute("SELECT * FROM category")
            categories = cursor.fetchall()
            cursor.execute("SELECT * FROM orders WHERE customer_ID=%s", (session['user'][0],))
            user_orders = cursor.fetchall()
            cursor.execute("SELECT * FROM order_items")
            order_items = cursor.fetchall()
            cursor.execute("SELECT * FROM cart_items WHERE cart_ID=%s", (session['user'][0],))
            cart_items = cursor.fetchall()
            cursor.close()
            return render_template('user_dashboard.html', products=products, categories=categories, 
                                orders=user_orders, order_items=order_items, cart_items=cart_items, 
                                cart_total=calculate_cart_total(cart_items, products)
                                )
        
        elif action == 'buy_now':
            cursor = mydb.cursor()
            cursor.execute("SELECT price FROM product WHERE product_ID=%s", (product_ID,))
            product_price = cursor.fetchone()[0]
            order_price = product_price * int(quantity)
            reduce_stock_query = "UPDATE product SET stockquantity = stockquantity - %s WHERE product_ID=%s"
            cursor.execute(reduce_stock_query, (quantity, product_ID))
            insert_order_query = "INSERT INTO orders (customer_ID, status) VALUES (%s, 'Processing')"
            cursor.execute(insert_order_query, (session['user'][0],))
            order_ID = cursor.lastrowid
            insert_order_item_query = "INSERT INTO order_items (order_ID, product_ID, quantity, price) VALUES (%s, %s, %s, %s)" 
            cursor.execute(insert_order_item_query, (order_ID, product_ID, quantity, order_price))
            mydb.commit()
            cursor.close()
            return redirect(url_for('user_dashboard'))

    else:
        return redirect(url_for('index'))

@app.route('/user_dashboard/update_cart/<int:product_ID>', methods=['POST'])
def update_cart(product_ID):
    if 'user' in session:
        quantity = request.form['quantity']

        cursor = mydb.cursor()
        cursor.execute("SELECT stockquantity FROM product WHERE product_ID=%s", (product_ID,))
        stock = cursor.fetchone()[0]
        if int(quantity) > stock:
            error = 'Quantity exceeds stock limit. Please try again.'
            return render_template('user_dashboard.html', error=error)
        cursor.execute("SELECT * FROM cart_items WHERE product_ID=%s AND cart_ID=%s", (product_ID, session['user'][0]))
        item = cursor.fetchone()

        if item:
            update_query = "UPDATE cart_items SET quantity=%s WHERE product_ID=%s AND cart_ID=%s"
            cursor.execute(update_query, (quantity, product_ID, session['user'][0]))
        else:
            insert_query = "INSERT INTO cart_items (product_ID, cart_ID, quantity) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (product_ID, session['user'][0], quantity))

        mydb.commit()
        cursor.execute("SELECT * FROM product")
        products = cursor.fetchall()
        cursor.execute("SELECT * FROM category")
        categories = cursor.fetchall()
        cursor.execute("SELECT * FROM orders WHERE customer_ID=%s", (session['user'][0],))
        user_orders = cursor.fetchall()
        cursor.execute("SELECT * FROM order_items")
        order_items = cursor.fetchall()
        cursor.execute("SELECT * FROM cart_items WHERE cart_ID=%s", (session['user'][0],))
        cart_items = cursor.fetchall()
        cursor.close()
        return render_template('user_dashboard.html', products=products, categories=categories, 
                               orders=user_orders, order_items=order_items, cart_items=cart_items, 
                               cart_total=calculate_cart_total(cart_items, products)
                               )

    else:
        return redirect(url_for('index'))
    
@app.route('/user_dashboard/remove_from_cart/<int:product_ID>', methods=['POST'])
def remove_cart_item(product_ID):
    if 'user' in session:
        cursor = mydb.cursor()
        delete_query = "DELETE FROM cart_items WHERE product_ID=%s AND cart_ID=%s"
        cursor.execute(delete_query, (product_ID, session['user'][0]))
        mydb.commit()
        cursor.close()

        return redirect(url_for('user_dashboard'))
    else:
        return redirect(url_for('index'))

@app.route('/user_dashboard/checkout', methods=['POST'])
def checkout():
    if 'user' in session:
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM cart_items WHERE cart_ID=%s", (session['user'][0],))
        cart_items = cursor.fetchall()

        if not cart_items:
            error = 'Cart is empty. Please add items to cart before checking out.'
            return render_template('user_dashboard.html', error=error)
        # for item in cart_items:
        #     product_ID = item[1]
        #     quantity = item[2]
        #     stock = products[product_ID - 1][3]
        #     if quantity > stock:
        #         error = 'Quantity exceeds stock limit. Please try again.'
        #         return render_template('user_dashboard.html', stockerror=error)
        for item in cart_items:
            product_ID = item[1]
            quantity = item[2]
            cursor.execute("SELECT price FROM product WHERE product_ID=%s", (product_ID,))
            product_price = cursor.fetchone()[0]
            order_price = product_price * quantity
            reduce_stock_query = "UPDATE product SET stockquantity = stockquantity - %s WHERE product_ID=%s"
            cursor.execute(reduce_stock_query, (quantity, product_ID))
            insert_order_query = "INSERT INTO orders (customer_ID, status) VALUES (%s, 'Processing')"
            cursor.execute(insert_order_query, (session['user'][0],))
            order_ID = cursor.lastrowid
            insert_order_item_query = "INSERT INTO order_items (order_ID, product_ID, quantity, price) VALUES (%s, %s, %s, %s)" 
            cursor.execute(insert_order_item_query, (order_ID, product_ID, quantity, order_price))

        
        delete_cart_query = "DELETE FROM cart_items WHERE cart_ID=%s"
        cursor.execute(delete_cart_query, (session['user'][0],))

        mydb.commit()
        cursor.close()

        return redirect(url_for('user_dashboard'))
    
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
        try: 
            name = request.form['name']
            age = request.form['age']
            phone = request.form['phone']
            email = request.form['email']
            passwd =  ''.join(random.choices(string.ascii_uppercase +string.digits, k=8))

            cursor = mydb.cursor()
            insert_query = "INSERT INTO employee (empname, age, phone_no, email, passwd) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (name, age, phone, email, passwd))
            mydb.commit()
            cursor.close()

            return redirect(url_for('admin_dashboard'))
        except mysql.connector.Error as err:
            return render_template('admin_dashboard.html', ageerror=err.msg)
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
        cursor.execute("SELECT * FROM product")
        products = cursor.fetchall()
        print(len(products))
        cursor.close()

        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('index'))
    
@app.route('/admin_dashboard/delete_product/<int:product_ID>', methods=['GET'])
def delete_product(product_ID):
    if 'admin' in session:
        cursor = mydb.cursor()

        delete_queries = []
        delete_queries.append("DELETE FROM product_personalisation WHERE product_ID = %s")
        delete_queries.append("DELETE FROM order_items WHERE product_ID = %s")
        delete_queries.append("DELETE FROM cart_items WHERE product_ID = %s")
        delete_queries.append("DELETE FROM review WHERE product_ID = %s")
        delete_queries.append("DELETE FROM product WHERE product_ID = %s")

        for delete_query in delete_queries:
            cursor.execute(delete_query, (product_ID,))

        mydb.commit()
        cursor.close()

        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('index'))

@app.route('/admin_dashboard/edit_data/product/<int:product_ID>', methods=['GET', 'POST'])
def edit_product(product_ID):
    if 'admin' in session:
        if request.method == 'POST':
            name = request.form['productname']
            price = request.form['price']
            category_id = request.form['category_ID']
            stock = request.form['stockquantity']
            description = request.form['productdesc']

            cursor = mydb.cursor()
            update_query = "UPDATE product SET productname=%s, price=%s, category_ID=%s, stockquantity=%s, productdesc=%s WHERE product_ID=%s"
            cursor.execute(update_query, (name, price, category_id, stock, description, product_ID))
            mydb.commit()
            cursor.close()

            return redirect(url_for('admin_dashboard'))
        else:
            cursor = mydb.cursor()
            select_query = "SELECT * FROM product WHERE product_ID=%s"
            cursor.execute(select_query, (product_ID,))
            product_data = cursor.fetchone()
            cursor.close()

            product_dict = dict(zip([col[0] for col in cursor.description], product_data))

            return render_template('edit_data.html', table_name='product', data_id=product_ID, data=product_dict)
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
        delete_queries = []
        
        delete_queries.append("DELETE FROM product_personalisation WHERE product_ID IN (SELECT product_ID FROM product WHERE category_ID = %s)")
        delete_queries.append("DELETE FROM order_items WHERE product_ID IN (SELECT product_ID FROM product WHERE category_ID = %s)")
        delete_queries.append("DELETE FROM cart_items WHERE product_ID IN (SELECT product_ID FROM product WHERE category_ID = %s)")
        delete_queries.append("DELETE FROM review WHERE product_ID IN (SELECT product_ID FROM product WHERE category_ID = %s)")
        delete_queries.append("DELETE FROM product WHERE category_ID = %s")
        delete_queries.append("DELETE FROM category WHERE category_ID = %s")

        for delete_query in delete_queries:
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
        delete_queries = []

        delete_queries.append("DELETE FROM cart_items WHERE cart_ID IN (SELECT cart_ID FROM cart WHERE customer_ID = %s)")
        delete_queries.append("DELETE FROM cart WHERE customer_ID = %s")
        delete_queries.append("DELETE FROM review WHERE customer_ID = %s")
        delete_queries.append("DELETE FROM order_items WHERE order_ID IN (SELECT order_ID FROM orders WHERE customer_ID = %s)")
        delete_queries.append("DELETE FROM orders WHERE customer_ID = %s")
        delete_queries.append("DELETE FROM customer WHERE customer_ID = %s")

        for delete_query in delete_queries:
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
        delete_queries = []

        delete_queries.append("DELETE FROM order_items WHERE order_ID = %s")
        delete_queries.append("DELETE FROM orders WHERE order_ID = %s")

        for delete_query in delete_queries:
            cursor.execute(delete_query, (order_ID,))

        mydb.commit()
        cursor.close()

        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    mydb.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
