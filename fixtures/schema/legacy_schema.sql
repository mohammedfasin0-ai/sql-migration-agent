CREATE TABLE customers (
    customer_id NUMBER,
    first_name VARCHAR2(100),
    last_name VARCHAR2(100),
    email VARCHAR2(255),
    created_at DATE
);

CREATE TABLE orders (
    order_id NUMBER,
    customer_id NUMBER,
    order_date DATE,
    total_amount NUMBER(10, 2),
    status VARCHAR2(20)
);

CREATE TABLE order_items (
    order_id NUMBER,
    product_id NUMBER,
    quantity NUMBER
);

CREATE TABLE products (
    product_id NUMBER,
    product_name VARCHAR2(255),
    category VARCHAR2(100)
);

CREATE TABLE employees (
    employee_id NUMBER,
    first_name VARCHAR2(100),
    last_name VARCHAR2(100),
    department VARCHAR2(100)
);