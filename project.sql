CREATE DATABASE IF NOT EXISTS Bills;
USE Bills;

CREATE TABLE IF NOT EXISTS Users (
    user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL
);


CREATE TABLE IF NOT EXISTS Invoices (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    provider VARCHAR(100) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    due_date DATE NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);


CREATE TABLE IF NOT EXISTS Payments (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    amount DECIMAL(10,2) NOT NULL,
    payment_date DATE NOT NULL,
    method ENUM('Cash', 'Credit Card', 'Debit Card') NOT NULL,
    bill_id INT NOT NULL,
    FOREIGN KEY (bill_id) REFERENCES Invoices(id)
);


CREATE TABLE IF NOT EXISTS WaterBills (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    provider VARCHAR(100),
    amount DECIMAL(10,2),
    due_date DATE,
    consumption_m3 DECIMAL(10,2),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE IF NOT EXISTS ElectricityBills (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    provider VARCHAR(100),
    amount DECIMAL(10,2),
    due_date DATE,
    kwh_used DECIMAL(10,2),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE IF NOT EXISTS InternetBills (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    provider VARCHAR(100),
    amount DECIMAL(10,2),
    due_date DATE,
    data_gb DECIMAL(10,2),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);
