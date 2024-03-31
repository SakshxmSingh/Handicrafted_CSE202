# CSE202_DBMS_Proj - Handicrafted.in
group course project for CSE202 - Fundamentals of Database Management Systems at IIIT-D
- Adya Aggarwal
- Kirti Jain
- Dhruv Prakash
- Saksham Singh

## Overview
This Flask application is designed for managing a handicrafts website, including user and admin functionalities such as login/logout, product management, cart handling, checkout, and more.

## Prerequisites
- Python 3.x installed
- MySQL database server
- Flask and MySQL Connector/Python libraries

## Setup
1. Clone this repository to your local machine.
2. Create a virtual environment:
    ```bash
    python -m venv venv
    ```
3. Activate the virtual environment:
    - Windows:
        ```bash
        venv\Scripts\activate
        ```
    - macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
4. Install the required packages:
    ```bash
    pip install flask mysql-connector-python
    ```
5. Set up your MySQL database and update the connection details in `app.py`.

## Running the Application
1. Activate the virtual environment if not already activated.
2. Run the Flask application:
    ```bash
    python app.py
    ```
3. Open your web browser and go to `http://localhost:5000` to access the application.

## Application Structure
- `app.py`: Contains the Flask application code.
- `templates/`: Directory for HTML templates.
- `static/`: Directory for static files like CSS, JavaScript, and images.

## Features
- User Authentication: Login/logout functionality for users and admins.
- User Dashboard: Browse products, search/filter, manage cart, and checkout.
- Admin Dashboard: Manage employees, products, categories, customers, and orders.

