CREATE DATABASE IF NOT EXISTS airsoftdb;

USE airsoftdb;

CREATE TABLE IF NOT EXISTS Accounts (
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
	is_admin BOOLEAN DEFAULT FALSE,
	elo INT
);


CREATE TABLE IF NOT EXISTS Reservations (
	id INT AUTO_INCREMENT PRIMARY KEY,
	account_id INT NOT NULL,
	game_mode_id INT NOT NULL,
	map_id INT NOT NULL,
	created_at DATETIME,
	equipment_kit_id INT NOT NULL,
	price INT NOT NULL,
	reservation_date DATE NOT NULL,
	start_time TIME,
	end_time TIME,
	is_public BOOLEAN,
	canceled BOOLEAN DEFAULT FALSE,
	cancelation_reason VARCHAR(500),
	UNIQUE KEY uq_map_slot (map_id, reservation_date, start_time),
	CHECK (
		canceled = TRUE OR (
			HOUR(start_time) IN (5,7,9,11,13,15,17,19)
			AND end_time = ADDTIME(start_time, '02:00:00')
		)
	)
);


CREATE TABLE IF NOT EXISTS RegisteredPlayers (
	id INT AUTO_INCREMENT PRIMARY KEY,
	reservation_id INT NOT NULL,
	account_id INT NOT NULL,
	created_at DATE
);


CREATE TABLE IF NOT EXISTS EquipmentKit (
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	brand VARCHAR(100),
	price FLOAT,
	quantity INT NOT NULL DEFAULT 1,
	purchase_link VARCHAR(500)
);

INSERT IGNORE INTO EquipmentKit (id, name, brand, price, quantity) VALUES
(1, 'Kit Básico', 'Valken', 2000, 10),
(2, 'Kit Intermedio', 'Lancer Tactical', 3500, 5),
(3, 'Kit Profesional', 'G&G Armament', 5000, 3);


CREATE TABLE IF NOT EXISTS Maps (
	id INT AUTO_INCREMENT PRIMARY KEY,
	image_url VARCHAR(100),
	name VARCHAR(100) UNIQUE,
	description VARCHAR(900)
);

INSERT IGNORE INTO Maps (name, description) VALUES
('Nuketown', 'Mapa clásico de combate urbano'),
('Mirage', 'Mapa táctico con zonas desérticas'),
('Hijacked', 'Mapa ambientado en un yate de lujo'),
('Terminal', 'Mapa ambientado en un aeropuerto');

INSERT IGNORE INTO Accounts (id, name, username, email, password, dni, phone, about_me, created_at, updated_at, is_active, is_admin)
VALUES (1, 'Juan Perez', 'juanperez', 'juanperez@email.com', '123456', '12345678', '123456789', 'Jugador de airsoft', NOW(), NOW(), TRUE, FALSE);


CREATE TABLE IF NOT EXISTS Review (
	id INT AUTO_INCREMENT PRIMARY KEY,
	stars INT NOT NULL CHECK (stars BETWEEN 1 AND 5),
	body_review VARCHAR(900),
	map_id INT NOT NULL,
	created_at DATE,
	approved BOOLEAN
);


CREATE TABLE IF NOT EXISTS GameModes (
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(75) NOT NULL,
	duration ENUM('30', '60', '90', '120') NOT NULL,
	players INT NOT NULL,
	updated_at DATE
);

INSERT IGNORE INTO GameModes (name, duration, players) VALUES
('Todos vs Todos', '60', 20),
('Captura la bandera', '90', 20),
('Duelo por equipos', '60', 10),
('Rey de la colina', '120', 20);