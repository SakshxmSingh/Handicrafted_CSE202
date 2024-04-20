import threading
import pymysql
import time

# Function to simulate purchasing a product
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
            # Get initial stock quantity
            cursor.execute(f"SELECT stockquantity FROM product WHERE product_ID = {product_id};")
            initial_stock_quantity = cursor.fetchone()['stockquantity']
            print(f"Initial Stock Quantity for Product {product_id}: {initial_stock_quantity}")

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

            # Get final stock quantity
            cursor.execute(f"SELECT stockquantity FROM product WHERE product_ID = {product_id};")
            final_stock_quantity = cursor.fetchone()['stockquantity']
            print(f"Final Stock Quantity for Product {product_id}: {final_stock_quantity}")

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

# Parameters for the transactions
customer_id1 = 1
product_id = 3  # Assuming both customers are trying to buy the same product
quantity = 1
order_status = 'Completed'

# Creating threads
thread1 = threading.Thread(target=buy_product, args=(customer_id1, product_id, quantity, order_status))
thread2 = threading.Thread(target=buy_product, args=(customer_id1 + 1, product_id, quantity, order_status))  # Increment customer ID for simplicity

# Starting threads
thread1.start()
thread2.start()

# Adding a delay to make sure conflicts can occur
time.sleep(1)

# Joining threads to the main thread
thread1.join()
thread2.join()