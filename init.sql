CREATE DATABASE IF NOT EXISTS university_db;
USE university_db;

CREATE TABLE IF NOT EXISTS subscriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255),
    plan_type VARCHAR(50),
    amount DECIMAL(10, 2),
    start_date DATE,
    end_date DATE
);

CREATE TABLE IF NOT EXISTS payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255),
    sub_id INT,
    amount DECIMAL(10, 2),
    status VARCHAR(50),
    payment_date DATETIME
);

CREATE TABLE IF NOT EXISTS logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    service VARCHAR(255),
    level VARCHAR(50),
    message TEXT
);
