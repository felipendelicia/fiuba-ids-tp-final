CREATE DATABASE IF NOT EXISTS airsoftdb;

USE airsoftdb;

CREATE TABLE IF NOT EXISTS Accounts {
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	username VARCHAR(100) NOT NULL,
	email VARCHAR(100) UNIQUE NOT NULL,
	password VARCHAR(150) NOT NULL,
	dni VARCHAR(20) NOT NULL UNIQUE,
	gender FLOAT,
	phone VARCHAR(30),
	about_me TEXT,
	created_at DATETIME,
	updated_at DATETIME NOT NULL,
	last_reservation DATE,
	is_active BOOLEAN DEFAULT TRUE,
	elo INT
};


CREATE TABLE IF NOT EXISTS Reservations {
	id INT AUTO_INCREMENT PRIMARY KEY,
	account_id INT NOT NULL,
	game_mode_id INT NOT NUL,
	map_id INT NOT NULL,
	created_at DATETIME,
	equipment_kit_id INT NOT NULL,
	price INT NOT NULL,
	reservation_date DATE NOT NULL,
	start_time DATE,
	end_time DATE,
	is_public BOOLEAN,
	canceled BOOLEAN DEFAULT FALSE,
	cancelation_reason VARCHAR
};


CREATE TABLE IF NOT EXISTS RegisteredPlayers {
	id INT AUTO_INCREMENT PRIMARY KEY,
	reservation_id INT NOT NULL,
	account_id INT NOT NULL,
	created_at DATE
};


CREATE TABLE IF NOT EXISTS EquipmentKit {
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	brand VARCHAR(100),
	price FLOAT
};


CREATE TABLE IF NOT EXISTS Maps {
	id INT AUTO_INCREMENT PRIMARY KEY,
	image_url VARCHAR(100),
	name VARCHAR(100),
	description VARCHAR(900)
};


CREATE TABLE IF NOT EXISTS Review {
	id INT AUTO_INCREMENT PRIMARY KEY,
	stars INT NOT NULL CHECK (stars BETWEEN 1 AND 5)
	body_review VARCHAR(900)
	map_id INT NOT NULL,
	created_at DATE,
	approved BOOLEAN
};


CREATE TABLE IF NOT EXISTS GameModes {
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(75) NOT NULL,
	duration ENUM('30', '60', '90', '120') NOT NULL,
	players INT NOT NULL,
	updated_at DATE
};



