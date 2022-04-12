-- Re/create DB
DROP DATABASE IF EXISTS trade_site;
CREATE DATABASE trade_site;
USE trade_site;

-- Create trade site table

CREATE TABLE users(
id VARCHAR(25),
user_name VARCHAR(25) PRIMARY KEY,
email VARCHAR(50),
user_password VARCHAR(255),
shipping_address VARCHAR(255),
reputation FLOAT,
FOREIGN KEY (id) REFERENCES users(user_name)
);


CREATE TABLE IF NOT EXISTS trades(
trade_id INT PRIMARY KEY AUTO_INCREMENT,
item_desc TEXT,
item_type CHAR(12),
item_name VARCHAR(50),
item_condition CHAR(12),
completed_trade BOOLEAN,
active_trade BOOLEAN,
trade_date datetime,
user_name VARCHAR(25),
FOREIGN KEY (user_name) REFERENCES users (user_name)
);

CREATE TABLE IF NOT EXISTS wishlist(
wishitem_id INT PRIMARY KEY AUTO_INCREMENT,
item_name CHAR(50),
user_name VARCHAR(25),
FOREIGN KEY (user_name) REFERENCES users (user_name)
);


CREATE TABLE IF NOT EXISTS notes(
note_id INT PRIMARY KEY AUTO_INCREMENT,
note_data VARCHAR(255) NOT NULL,
post_date datetime,
user_name VARCHAR(25),
trade_id INT,
FOREIGN KEY (user_name) REFERENCES users (user_name),
FOREIGN KEY (trade_id) REFERENCES trades (trade_id)
);

Select * from users;