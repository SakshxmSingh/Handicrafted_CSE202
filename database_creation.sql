DROP DATABASE IF EXISTS handicrafted;
CREATE SCHEMA handicrafted;
USE handicrafted;

CREATE TABLE category (
    category_ID INT AUTO_INCREMENT PRIMARY KEY,
    catname VARCHAR(255) NOT NULL,
    catdesc VARCHAR(255) NOT NULL
);

CREATE TABLE personalisation (
    personalisation_ID INT AUTO_INCREMENT PRIMARY KEY,
    persname VARCHAR(255) NOT NULL,
    addinfo VARCHAR(255) NOT NULL
);


CREATE TABLE product (
    product_ID INT AUTO_INCREMENT PRIMARY KEY,
    productname VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stockquantity INT NOT NULL,
    productdesc VARCHAR(255) NOT NULL,
    category_ID INT,
    FOREIGN KEY (category_ID) REFERENCES category(category_ID)
);

CREATE TABLE product_personalisation (
    product_ID INT,
    personalisation_ID INT,
    PRIMARY KEY (product_ID, personalisation_ID),
    FOREIGN KEY (product_ID) REFERENCES product(product_ID),
    FOREIGN KEY (personalisation_ID) REFERENCES personalisation(personalisation_ID)
);


CREATE TABLE customer (
    customer_ID INT AUTO_INCREMENT PRIMARY KEY,
    fullname VARCHAR(255) NOT NULL,
    phone_no VARCHAR(20) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    address VARCHAR(255) NOT NULL,
    passwd VARCHAR(255) NOT NULL
);

CREATE TABLE cart (
    cart_ID INT AUTO_INCREMENT PRIMARY KEY,
    customer_ID INT,
    FOREIGN KEY (customer_ID) REFERENCES customer(customer_ID)
);

CREATE TABLE cart_items (
    cart_ID INT,
    product_ID INT,
    quantity INT NOT NULL,
    PRIMARY KEY (cart_ID, product_ID),
    FOREIGN KEY (cart_ID) REFERENCES cart(cart_ID),
    FOREIGN KEY (product_ID) REFERENCES product(product_ID)
);

CREATE TABLE review (
    review_ID INT AUTO_INCREMENT PRIMARY KEY,
    product_ID INT,
    customer_ID INT,
    subj VARCHAR(255) NOT NULL,
    descptn TEXT NOT NULL,
    rating INT NOT NULL,
    FOREIGN KEY (product_ID) REFERENCES product(product_ID),
    FOREIGN KEY (customer_ID) REFERENCES customer(customer_ID)
);

CREATE TABLE orders (
    order_ID INT AUTO_INCREMENT PRIMARY KEY,
    customer_ID INT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50),
    FOREIGN KEY (customer_ID) REFERENCES customer(customer_ID)
);

CREATE TABLE order_items (
    order_ID INT,
    product_ID INT,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (order_ID, product_ID),
    FOREIGN KEY (order_ID) REFERENCES orders(order_ID),
    FOREIGN KEY (product_ID) REFERENCES product(product_ID)
);

CREATE TABLE employee (
    employee_ID INT AUTO_INCREMENT PRIMARY KEY,
    empname VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    phone_no VARCHAR(20) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    passwd VARCHAR(255) NOT NULL
);

CREATE TABLE admins (
    admin_ID INT AUTO_INCREMENT PRIMARY KEY,
    adminame VARCHAR(255) NOT NULL,
    phone_no VARCHAR(20) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    passwd VARCHAR(255) NOT NULL
);



-- Display all tables in the current database
/*
DESCRIBE category;
DESCRIBE product;
DESCRIBE customer;
DESCRIBE review;
DESCRIBE orders;
DESCRIBE order_items;
DESCRIBE employee;
DESCRIBE admins;
DESCRIBE employee_products;
DESCRIBE admin_products;
DESCRIBE employee_orders;
DESCRIBE admin_orders;
*/

INSERT INTO category (catname, catdesc) VALUES
('Photo Frames', 'Decorative frames to display your cherished memories.'),
('T-shirts', 'Comfortable and stylish t-shirts in various designs.'),
('Mugs', 'Customizable mugs for your coffee and tea.'),
('Caps', 'Fashionable caps suitable for every occasion.'),
('Sneakers', 'Durable and trendy sneakers for everyday wear.'),
('Mobile Covers', 'Protective and stylish covers for different mobile models.'),
('Mirrors', 'Decorative mirrors to enhance your living spaces.'),
('Laptop Skins', 'Customizable skins to personalize your laptops.'),
('Crochet Keychains', 'Handmade crochet keychains in various designs.'),
('Notebooks', 'Notebooks for your writing, notes, and sketches.');

INSERT INTO product (productname, price, stockquantity, productdesc, category_ID) VALUES
('Vintage Wood Frame', 350, 15, 'A classic vintage wood photo frame.', 1),
('Graphic Tee', 250, 30, 'Cotton graphic tee with a round neck.', 2),
('Ceramic Mug', 200, 40, 'High-quality ceramic mug.', 3),
('Baseball Cap', 220, 25, 'Adjustable baseball cap in various colors.', 4),
('Running Sneakers', 1200, 20, 'Lightweight running sneakers for optimal performance.', 5),
('Leather Mobile Cover', 450, 30, 'Premium leather cover for smartphones.', 6),
('Wall Hanging Mirror', 750, 10, 'Elegant wall hanging mirror for decor.', 7),
('Floral Laptop Skin', 300, 25, 'Floral design laptop skin for 15-inch laptops.', 8),
('Elephant Crochet Keychain', 210, 50, 'Handmade elephant crochet keychain.', 9),
('Spiral Notebook', 210, 100, 'Spiral-bound notebook with lined pages.', 10);

INSERT INTO personalisation (persname, addinfo) VALUES
('Engraving', 'Custom text engraving on the product.'),
('Color', 'Choose a custom color for the product.'),
('Size', 'Specify a custom size.'),
('Material', 'Select from various material options.'),
('Print', 'Add a custom print or design.'),
('Embroidery', 'Custom embroidery options.'),
('Packaging', 'Special packaging options.'),
('Accessory', 'Add custom accessories.'),
('Message', 'Include a personalized message.'),
('Finish', 'Choose a specific finish for the product.');

INSERT INTO customer (fullname, phone_no, email, address, passwd) VALUES
('Priya Kumar', '1234567890', 'priya.kumar@email.com', 'Mumbai, Maharashtra', 'password123'),
('Amit Shah', '0987654321', 'amit.shah@email.com', 'New Delhi, Delhi', 'password456'),
('Sunita Gupta', '1122334455', 'sunita.gupta@email.com', 'Bangalore, Karnataka', 'password789'),
('Rahul Singh', '2233445566', 'rahul.singh@email.com', 'Kolkata, West Bengal', 'password101'),
('Anjali Rao', '3344556677', 'anjali.rao@email.com', 'Chennai, Tamil Nadu', 'password102'),
('Mohit Patil', '4455667788', 'mohit.patil@email.com', 'Pune, Maharashtra', 'password103'),
('Neha Malik', '5566778899', 'neha.malik@email.com', 'Jaipur, Rajasthan', 'password104'),
('Vijay Kumar', '6677889900', 'vijay.kumar@email.com', 'Hyderabad, Telangana', 'password105'),
('Sara Ali', '7788990011', 'sara.ali@email.com', 'Ahmedabad, Gujarat', 'password106'),
('Karan Singh', '8899001122', 'karan.singh@email.com', 'Surat, Gujarat', 'password107');

INSERT INTO cart (customer_ID) VALUES
(1), (2), (3), (4), (5), (6), (7), (8), (9), (10);

INSERT INTO cart_items (cart_ID, product_ID, quantity) VALUES
(1, 1, 1), (1, 2, 1), -- Customer 1 adds 2 products
(2, 3, 2), -- Customer 2 adds 1 product but 2 quantities
(3, 4, 1), (3, 5, 1), -- Customer 3 adds 2 products
(4, 6, 1), -- Customer 4 adds 1 product
(5, 7, 1), (5, 8, 1), -- Customer 5 adds 2 products
(6, 9, 2), -- Customer 6 adds 1 product but 2 quantities
(7, 10, 1), -- Customer 7 adds 1 product
(8, 1, 1), (8, 2, 1), -- Customer 8 adds 2 products
(9, 3, 1), -- Customer 9 adds 1 product
(10, 4, 2); -- Customer 10 adds 1 product but 2 quantities

INSERT INTO product_personalisation (product_ID, personalisation_ID) VALUES
(1, 1), (1, 2),
(2, 3), (2, 4),
(3, 5), (3, 6),
(4, 7), (4, 8),
(5, 9), (5, 10),
(6, 1), (6, 2),
(7, 3), (7, 4),
(8, 5), (8, 6),
(9, 7), (9, 8),
(10, 9), (10, 10);

INSERT INTO review (product_ID, customer_ID, subj, descptn, rating) VALUES
(1, 1, 'Love the Vintage Look', 'The vintage wood frame adds a classic touch to my room.', 5),
(2, 2, 'Great Quality Tee', 'The graphic tee is really comfortable and the print is durable.', 4),
(3, 3, 'Perfect for Coffee', 'This ceramic mug has become my go-to for morning coffee.', 5),
(4, 4, 'Stylish and Comfortable', 'The baseball cap fits perfectly and looks great.', 4),
(5, 5, 'Best Sneakers Ever', 'These sneakers are comfortable and perfect for running.', 5),
(6, 6, 'High-Quality Cover', 'The leather mobile cover is durable and looks premium.', 4),
(7, 7, 'Beautiful Mirror', 'The wall hanging mirror is elegant and enhances my living room.', 5),
(8, 8, 'Lovely Laptop Skin', 'The floral laptop skin is beautiful and easy to apply.', 4),
(9, 9, 'Cute Keychain', 'The crochet elephant keychain is adorable and well-made.', 5),
(10, 10, 'Useful Notebook', 'The spiral notebook is handy for my daily notes.', 4);

INSERT INTO orders (customer_ID, order_date, status) VALUES
(1, '2024-02-10', 'Delivered'),
(2, '2024-02-11', 'Shipped'),
(3, '2024-02-12', 'Processing'),
(4, '2024-02-09', 'Delivered'),
(5, '2024-02-08', 'Shipped'),
(6, '2024-02-07', 'Processing'),
(7, '2024-02-06', 'Delivered'),
(8, '2024-02-05', 'Shipped'),
(9, '2024-02-04', 'Processing'),
(10, '2024-02-03', 'Delivered');

INSERT INTO order_items (order_ID, product_ID, quantity, price) VALUES
(1, 1, 1, 350),
(2, 2, 2, 250),
(3, 3, 1, 200),
(4, 4, 1, 220),
(5, 5, 1, 1200),
(6, 6, 1, 450),
(7, 7, 1, 750),
(8, 8, 1, 300),
(9, 9, 2, 210),
(10, 10, 3, 210);

INSERT INTO employee (empname, age, phone_no, email, passwd) VALUES
('Rohan Mehra', '30', '1231231230', 'rohan.mehra@email.com', 'emp123'),
('Anita Desai', '45', '3213213210', 'anita.desai@email.com', 'emp456'),
('Vikram Reddy', '42', '4564564560', 'vikram.reddy@email.com', 'emp789'),
('Meera Chopra', '28', '6546546540', 'meera.chopra@email.com', 'emp101'),
('Suresh Kumar', '32', '7897897890', 'suresh.kumar@email.com', 'emp102'),
('Deepika Rao', '30', '8908908901', 'deepika.rao@email.com', 'emp103'),
('Manish Singh', '27', '9019019012', 'manish.singh@email.com', 'emp104'),
('Kriti Joshi', '27','0120120123', 'kriti.joshi@email.com', 'emp105'),
('Aryan Khanna', '37','1231231234', 'aryan.khanna@email.com', 'emp106'),
('Simran Kaur', '42', '2342342345', 'simran.kaur@email.com', 'emp107');

INSERT INTO admins (adminame, phone_no, email, passwd) VALUES
('Aditya Singh', '9879879870', 'aditya.singh@email.com', 'admin123'),
('Priyanka Iyer', '7897897891', 'priyanka.iyer@email.com', 'admin456'),
('Nikhil Sharma', '6786786782', 'nikhil.sharma@email.com', 'admin789'),
('Anushka Verma', '5675675673', 'anushka.verma@email.com', 'admin101'),
('Rajat Gupta', '4564564564', 'rajat.gupta@email.com', 'admin102'),
('Sonal Singh', '3453453455', 'sonal.singh@email.com', 'admin103'),
('Vivek Patel', '2342342346', 'vivek.patel@email.com', 'admin104'),
('Ishaan Das', '1231231237', 'ishaan.das@email.com', 'admin105'),
('Monica Roy', '0120120128', 'monica.roy@email.com', 'admin106'),
('Ajay Kumar', '9019019019', 'ajay.kumar@email.com', 'admin281');

SELECT * FROM category;
SELECT * FROM product;
SELECT * FROM product_personalisation;
SELECT * FROM cart;
SELECT * FROM cart_items;
SELECT * FROM customer;
SELECT * FROM review;
SELECT * FROM orders;
SELECT * FROM order_items;
SELECT * FROM employee;
SELECT * FROM admins;


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