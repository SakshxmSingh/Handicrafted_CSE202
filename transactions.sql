
/* Placing a direct order : When directly buying a product (not from the cart), the product should be added to order, the stock quantity updated, the order status updated. */
START TRANSACTION;

-- Insert a new order for customer with customer_ID 1, directly buying product 3
INSERT INTO orders (customer_ID, status) VALUES (1, 'Processing');

-- Get the order ID for the newly created order
SET @new_order_id = LAST_INSERT_ID();

-- Add the purchased product to the order items
INSERT INTO order_items (order_ID, product_ID, quantity, price) VALUES (@new_order_id, 3, 1, (SELECT price FROM product WHERE product_ID = 3));

-- Update stock quantity for the purchased product
UPDATE product SET stockquantity = stockquantity - 1 WHERE product_ID = 3;

-- Change the order status to 'Completed'
UPDATE orders SET status = 'Placed' WHERE order_ID = @new_order_id;

COMMIT;


/* When placing an order from the cart, the cart should be emptied, the stock quantity updated, the order status updated. This should happen atomically. In case any step fails, the checkout fails. */

START TRANSACTION;

-- Customer with customer_ID 2 places an order for multiple products in their cart
INSERT INTO orders (customer_ID, status) VALUES (2, 'Processing');

-- Retrieve the newly created order ID
SET @new_order_id = LAST_INSERT_ID();

-- Transfer all cart items of customer 2 to order items
INSERT INTO order_items (order_ID, product_ID, quantity, price)
SELECT @new_order_id, product_ID, quantity, (SELECT price FROM product WHERE product.product_ID = cart_items.product_ID)
FROM cart_items
WHERE cart_ID = 2;

-- Update stock quantities based on the ordered quantities
UPDATE product
SET stockquantity = stockquantity - (SELECT quantity FROM order_items WHERE order_items.product_ID = product.product_ID AND order_ID = @new_order_id)
WHERE product_ID IN (SELECT product_ID FROM cart_items WHERE cart_ID = 2);

-- Empty the cart after placing the order
DELETE FROM cart_items WHERE cart_ID = 2;

-- Update the order status to 'Completed'
UPDATE orders SET status = 'Completed' WHERE order_ID = @new_order_id;

COMMIT;


/* When inserting a new customer, a new cart should be created automatically. If this fails, then the new customer should not be added. */

INSERT INTO customer (fullname, phone_no, email, address, passwd) 
VALUES ('John Doe', '9876543210', 'john.doe@email.com', '1234 Street, City, State', 'securePass123');

-- Get the customer ID
SET @new_customer_id = LAST_INSERT_ID();

-- Create an empty cart for the new customer
INSERT INTO cart (customer_ID) VALUES (@new_customer_id);

COMMIT;



/* Editing customer information: Either all the information should be update, or none. If a customer is updating their address and email, both should get updated together, or neither should be updated. */

START TRANSACTION;

-- Update profile information for customer with customer_ID 8
UPDATE customer
SET 
    fullname = 'John Doe Updated',
    phone_no = '9999999999',
    email = 'john.doe.updated@email.com',
    address = 'Updated Address, New City, New State',
    passwd = 'newSecurePassword987'
WHERE customer_ID = 8;

-- Commit the changes
COMMIT;









/*
CREATE INDEX idx_category_id ON product(category_ID);
CREATE INDEX idx_customer_email ON customer(email);
CREATE INDEX idx_product_id ON product_personalisation(product_ID);
CREATE INDEX idx_personalisation_id ON product_personalisation(personalisation_ID);
CREATE INDEX idx_cart_customer_id ON cart(customer_ID);
CREATE INDEX idx_cart_items_cart_id ON cart_items(cart_ID);
CREATE INDEX idx_cart_items_product_id ON cart_items(product_ID);
CREATE INDEX idx_review_product_id ON review(product_ID);
CREATE INDEX idx_review_customer_id ON review(customer_ID);
CREATE INDEX idx_orders_customer_id ON orders(customer_ID);
CREATE INDEX idx_order_items_order_id ON order_items(order_ID);
CREATE INDEX idx_order_items_product_id ON order_items(product_ID);
CREATE INDEX idx_employee_email ON employee(email);
CREATE INDEX idx_admins_email ON admins(email);
*/

/* Contributions:
Table creation: Dhruv & Kirti
Table population: Adya & Saksham
*/