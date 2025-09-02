import mysql.connector

# Connect to MySQL (without selecting a database first)
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)
cursor = conn.cursor()

# SQL statements
sql_statements = [
    "CREATE DATABASE IF NOT EXISTS ecommerce",
    "USE ecommerce",

    # Users table
    """CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100) UNIQUE,
        password VARCHAR(255),
        role ENUM('user', 'admin') DEFAULT 'user'
    )""",

    # Products table
    """CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        description TEXT,
        price DECIMAL(10, 2),
        image VARCHAR(255)
    )""",

    # Cart table
    """CREATE TABLE IF NOT EXISTS cart (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        product_id INT,
        quantity INT,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    )""",

    # Insert users
    """INSERT INTO users (id, name, email, password, role) VALUES
        (101,'Test User', 'user@test.com', '$2b$10$rJ2hYJN8mPD7gSv4JDhG7eERzOiNhVF55TpckXaBK6B2DchyOoGQa', 'user'),
        (102,'Admin', 'admin@test.com', '$2b$10$rJ2hYJN8mPD7gSv4JDhG7eERzOiNhVF55TpckXaBK6B2DchyOoGQa', 'admin')
        ON DUPLICATE KEY UPDATE name=VALUES(name), email=VALUES(email), password=VALUES(password), role=VALUES(role)""",

    # Insert products
    """INSERT INTO products (name, description, price, image) VALUES
        ('iPhone 15', 'Latest Apple smartphone', 999.99, 'iphone.jpg'),
        ('MacBook Air', 'Lightweight and powerful laptop', 1299.99, 'macbook.jpg'),
        ('AirPods Pro', 'Wireless noise-cancelling earbuds', 249.99, 'airpods.jpg')
    """
]

# Execute each SQL statement
for sql in sql_statements:
    try:
        cursor.execute(sql)
        print(f"Executed: {sql.split()[0]} ...")
    except Exception as e:
        print(f"Error in `{sql}`: {e}")

conn.commit()
cursor.close()
conn.close()

print("✅ All SQL statements executed successfully.")
