-- Checks for incorrect customer login, can be used same way for admin login
DELIMITER //

CREATE TRIGGER before_customer_login
BEFORE INSERT ON customer
FOR EACH ROW
BEGIN
    DECLARE v_correct_pass VARCHAR(255);
    
    SELECT passwd INTO v_correct_pass
    FROM customer
    WHERE email = NEW.email;
    
    IF v_correct_pass <> NEW.passwd THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Incorrect email or password';
    END IF;
END //

DELIMITER ;

DELIMITER //

CREATE TRIGGER before_admin_login
BEFORE INSERT ON admins
FOR EACH ROW
BEGIN
    DECLARE v_correct_pass VARCHAR(255);

    -- Check if the provided password matches the actual password for the admin
    SELECT passwd INTO v_correct_pass
    FROM admins
    WHERE email = NEW.email;

    -- If the provided password is incorrect, raise an error
    IF v_correct_pass <> NEW.passwd THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Incorrect email or password';
    END IF;
END //

DELIMITER ;


-- Checks if cart not empty before checkout
DELIMITER //

CREATE TRIGGER before_order_insert
BEFORE INSERT ON orders
FOR EACH ROW
BEGIN
    DECLARE cart_count INT;
    
    -- Check the number of items in the customer's cart
    SELECT COUNT(*) INTO cart_count
    FROM cart_items
    WHERE cart_ID = (SELECT cart_ID FROM cart WHERE customer_ID = NEW.customer_ID);
    
    -- If the cart is empty, raise an error
    IF cart_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot checkout with an empty cart';
    END IF;
END //

DELIMITER ;

-- checks employee's age
DELIMITER //

CREATE TRIGGER check_employee_age
BEFORE INSERT ON employee
FOR EACH ROW
BEGIN
    IF NEW.age < 25 OR NEW.age > 55 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Employee age must be between 25 and 55';
    END IF;
END //

DELIMITER ;