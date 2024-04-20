import threading
import pymysql
import time

# Function to simulate purchasing a product by a customer
def buy_product(customer_id, product_id, quantity, order_status):
    # Establishing the database connection
    connection = pymysql.connect(host='localhost', 
                                 user='root', 
                                 password='12345678', 
                                 db='handicrafted', 
                                 charset='utf8mb4', 
                                 cursorclass=pymysql.cursors.DictCursor)
    
    try:
        with connection.cursor() as cursor:
            # Start transaction
            cursor.execute("START TRANSACTION;")
            print(f"Transaction started for Customer {customer_id} buying Product {product_id}")

            # Insert a new order
            cursor.execute(f"INSERT INTO orders (customer_ID, status) VALUES ({customer_id}, 'Processing');")
            new_order_id = connection.insert_id()
            print(f"Order ID {new_order_id} created for Customer {customer_id}")

            # Add the purchased product to the order items with specified quantity
            cursor.execute(f"SELECT price FROM product WHERE product_ID = {product_id};")
            price = cursor.fetchone()['price']
            cursor.execute(f"INSERT INTO order_items (order_ID, product_ID, quantity, price) VALUES ({new_order_id}, {product_id}, {quantity}, {price});")
            print(f"Product {product_id} added to Order {new_order_id}")

            # Update stock quantity for the purchased product
            cursor.execute(f"UPDATE product SET stockquantity = stockquantity - {quantity} WHERE product_ID = {product_id};")
            print(f"Stock updated for Product {product_id}")

            # Change the order status
            cursor.execute(f"UPDATE orders SET status = '{order_status}' WHERE order_ID = {new_order_id};")
            print(f"Order {new_order_id} status changed to {order_status}")

            # Commit transaction
            connection.commit()
            print(f"Transaction committed for Customer {customer_id} buying Product {product_id}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        connection.rollback()
        print("Transaction rolled back due to an error")
    finally:
        connection.close()
        print("Database connection closed")

# Function to simulate an admin updating the stock quantity of a product
def update_stock(admin_id, product_id, new_stock_quantity):
    # Establishing the database connection
    connection = pymysql.connect(host='localhost', 
                                 user='root', 
                                 password='12345678', 
                                 db='handicrafted', 
                                 charset='utf8mb4', 
                                 cursorclass=pymysql.cursors.DictCursor)
    
    try:
        with connection.cursor() as cursor:
            # Start transaction
            cursor.execute("START TRANSACTION;")
            print(f"Transaction started for Admin {admin_id} updating stock quantity of Product {product_id}")

            # Update stock quantity for the product
            cursor.execute(f"UPDATE product SET stockquantity = {new_stock_quantity} WHERE product_ID = {product_id};")
            print(f"Stock quantity updated for Product {product_id}")

            # Commit transaction
            connection.commit()
            print(f"Transaction committed for Admin {admin_id} updating stock quantity")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        connection.rollback()
        print("Transaction rolled back due to an error")
    finally:
        connection.close()
        print("Database connection closed")

# Parameters for the transactions
product_id = 3  # Assuming both transactions involve Product 3
quantity = 1
order_status = 'Completed'
new_stock_quantity = 10  # New stock quantity to be set by the admin

# Creating threads for the customer buying and admin updating stock
thread1 = threading.Thread(target=buy_product, args=(1, product_id, quantity, order_status))  # Customer buying
thread2 = threading.Thread(target=update_stock, args=(1, product_id, new_stock_quantity))  # Admin updating stock

# Starting threads
thread1.start()
thread2.start()

# Joining threads to the main thread
thread1.join()
thread2.join()