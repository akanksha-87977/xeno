-- Create database
CREATE DATABASE IF NOT EXISTS transaction_validator;

-- Connect to database
\c transaction_validator;

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Customers table
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(100) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    email VARCHAR(255) NOT NULL,
    email_domain VARCHAR(100),
    is_gmail BOOLEAN DEFAULT FALSE,
    phone_number VARCHAR(50),
    city VARCHAR(100),
    signup_date DATE,
    signup_month VARCHAR(20),
    signup_day VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for customers
CREATE INDEX idx_customers_customer_id ON customers(customer_id);
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_city ON customers(city);
CREATE INDEX idx_customers_signup_date ON customers(signup_date);

-- Orders table
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    order_id VARCHAR(100) UNIQUE NOT NULL,
    customer_id VARCHAR(100) REFERENCES customers(customer_id),
    amount DECIMAL(10, 2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_orders_order_id ON orders(order_id);
CREATE INDEX idx_orders_customer_id ON orders(customer_id);

-- Transactions table
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(100) UNIQUE NOT NULL,
    order_id VARCHAR(100) REFERENCES orders(order_id),
    customer_id VARCHAR(100),
    customer_name VARCHAR(255),
    customer_email VARCHAR(255),
    customer_phone VARCHAR(50),
    country VARCHAR(10),
    city VARCHAR(100),
    product_id VARCHAR(100),
    product_name VARCHAR(255),
    quantity INTEGER,
    unit_price DECIMAL(10, 2),
    total_amount DECIMAL(10, 2),
    payment_mode VARCHAR(50),
    transaction_date DATE,
    transaction_time TIME,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_transactions_transaction_id ON transactions(transaction_id);
CREATE INDEX idx_transactions_order_id ON transactions(order_id);

-- VIP Customers table
CREATE TABLE vip_customers (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(100) NOT NULL,
    full_name VARCHAR(255),
    email VARCHAR(255),
    phone_number VARCHAR(50),
    city VARCHAR(100),
    signup_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Validation Reports table
CREATE TABLE validation_reports (
    id SERIAL PRIMARY KEY,
    report_id VARCHAR(100) UNIQUE NOT NULL,
    file_name VARCHAR(255),
    file_type VARCHAR(50),
    total_records INTEGER,
    valid_records INTEGER,
    invalid_records INTEGER,
    success_rate DECIMAL(5, 2),
    errors JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Uploaded Files table
CREATE TABLE uploaded_files (
    id SERIAL PRIMARY KEY,
    file_id VARCHAR(100) UNIQUE NOT NULL,
    file_name VARCHAR(255),
    file_type VARCHAR(50),
    file_path VARCHAR(500),
    row_count INTEGER,
    uploaded_by INTEGER REFERENCES users(id),
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Phone Validation Rules table
CREATE TABLE phone_validation_rules (
    id SERIAL PRIMARY KEY,
    country_code VARCHAR(10) UNIQUE NOT NULL,
    country_name VARCHAR(100),
    min_digits INTEGER,
    max_digits INTEGER,
    pattern VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Audit Logs table
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    log_id VARCHAR(100) UNIQUE NOT NULL,
    action VARCHAR(255) NOT NULL,
    user_id INTEGER REFERENCES users(id),
    details JSONB,
    ip_address VARCHAR(50),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp);