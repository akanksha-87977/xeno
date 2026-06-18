-- Seed phone validation rules
INSERT INTO phone_validation_rules (country_code, country_name, min_digits, max_digits, pattern) VALUES
('IN', 'India', 10, 10, '^[6-9][0-9]{9}$'),
('US', 'United States', 10, 10, '^[2-9][0-9]{9}$'),
('SG', 'Singapore', 8, 8, '^[689][0-9]{7}$'),
('GB', 'United Kingdom', 10, 11, '^[0-9]{10,11}$'),
('AU', 'Australia', 9, 9, '^[0-9]{9}$');

-- Create admin user (password: admin123)
INSERT INTO users (email, username, hashed_password, full_name, role) VALUES
('admin@example.com', 'admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5SdBwT8VCp6.e', 'System Admin', 'admin');

-- Sample customers
INSERT INTO customers (customer_id, full_name, first_name, email, email_domain, is_gmail, phone_number, city, signup_date, signup_month, signup_day) VALUES
('CUST001', 'Rajesh Kumar', 'Rajesh', 'rajesh@gmail.com', 'gmail.com', TRUE, '9876543210', 'Delhi', '2024-01-15', 'January', 'Monday'),
('CUST002', 'Priya Sharma', 'Priya', 'priya@yahoo.com', 'yahoo.com', FALSE, '9876543211', 'Mumbai', '2024-01-16', 'January', 'Tuesday'),
('CUST003', 'Amit Patel', 'Amit', 'amit@gmail.com', 'gmail.com', TRUE, '9876543212', 'Bangalore', '2024-01-17', 'January', 'Wednesday'),
('CUST004', 'Sneha Reddy', 'Sneha', 'sneha@outlook.com', 'outlook.com', FALSE, '9876543213', 'Hyderabad', '2024-01-18', 'January', 'Thursday'),
('CUST005', 'Vikram Singh', 'Vikram', 'vikram@gmail.com', 'gmail.com', TRUE, '9876543214', 'Chennai', '2024-01-19', 'January', 'Friday');