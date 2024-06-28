SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS Customers;
DROP TABLE IF EXISTS Accounts;
DROP TABLE IF EXISTS Transactions;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Support;

CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password_hash VARCHAR(300),
    role VARCHAR(20) DEFAULT 'user'
);

CREATE TABLE Customers (
    user_id INT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    address VARCHAR(100),
    phone VARCHAR(15),
    email VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Accounts (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    account_name VARCHAR(32),
    account_type VARCHAR(20),
    balance DECIMAL(15, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    account_id INT,
    dest_account_id INT,
    transaction_type VARCHAR(20),
    amount DECIMAL(15, 2),
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

INSERT INTO Users (user_id, username, password_hash, role) VALUES (1, 'admin', 'pbkdf2:sha256:260000$unHL6Wf1I4HwdLv8$6ef19d1510e90358130afcf456e72fcf8700bd5619d93488c1a390f8b6e65e0e', 'admin');
INSERT INTO Customers (user_id, first_name, last_name, address, phone, email) VALUES (1, 'admin', 'admin', 'flag{adminAddress}', '1557-1557', 'admin@admin.net');
INSERT INTO Accounts (account_id, user_id, account_name, account_type, balance) VALUES (1, 1, 'adminMoney', 'savings', 10000000);
SET FOREIGN_KEY_CHECKS=1;