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
	name VARCHAR(100) CHARACTER SET utf8mb4 NOT NULL,
	brand VARCHAR(100),
	price FLOAT,
	quantity INT NOT NULL DEFAULT 1,
	purchase_link VARCHAR(500)
) DEFAULT CHARSET=utf8mb4;

INSERT IGNORE INTO EquipmentKit (id, name, brand, price, quantity) VALUES
(1, 'Kit Básico', 'Valken', 2000, 10),
(2, 'Kit Intermedio', 'Lancer Tactical', 3500, 5),
(3, 'Kit Profesional', 'G&G Armament', 5000, 3);


CREATE TABLE IF NOT EXISTS Maps (
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(100) CHARACTER SET utf8mb4 UNIQUE,
    vista_general_image_url VARCHAR(100),
    plano_despliegue_image_url VARCHAR(100),
    operaciones_terreno_image_url VARCHAR(100),
	description VARCHAR(900) CHARACTER SET utf8mb4,
    capacity INT,
    extra_information VARCHAR(900) CHARACTER SET utf8mb4,
    location VARCHAR(100),
    style VARCHAR(100),
    terrain VARCHAR(100),
    difficulty ENUM('Fácil', 'Media', 'Difícil'),
    compatible_gamemodes VARCHAR(300),
    origin VARCHAR(100)
) DEFAULT CHARSET=utf8mb4;

INSERT IGNORE INTO Maps (
    vista_general_image_url,
    plano_despliegue_image_url,
    operaciones_terreno_image_url,
    name,
    description,
    capacity,
    extra_information,
    location,
    style,
    terrain,
    difficulty,
    compatible_gamemodes,
    origin
) VALUES
-- NUKETOWN
('nuketown.jpg', 'nuketown_2.png', 'nuketown_3.png', 'Nuketown',
 'Recreación de Nuketown 2025, el clásico escenario futurista popularizado por Call of Duty: Black Ops II. Inspirado en un vecindario construido para ensayos y demostraciones dentro de una instalación de pruebas nucleares, ofrece una distribución equilibrada que favorece partidas rápidas y enfrentamientos constantes entre ambos equipos.',
 10,
 'Nuketown 2025 es una recreación a escala real del famoso mapa de Call of Duty: Black Ops II. Ambientado en un vecindario suburbano construido dentro de una instalación de pruebas nucleares, ofrece un campo de batalla simétrico y equilibrado. Las dos casas enfrentadas, los vehículos en el frente y los patios traseros conforman el núcleo del combate. Su diseño promueve enfrentamientos rápidos, reflejos afilados y acción constante. Ideal para partidas casuales y torneos cortos donde la velocidad de reacción define al vencedor.',
 'Instalaciones Kinetix - Sector Alpha',
 'Combate rápido / Acción constante',
 'Urbano / Calles y edificios',
 'Media',
 'Team Deathmatch · Dominio · Captura la Bandera · Todos contra Todos',
 'Call of Duty: Black Ops II'),

-- MIRAGE
('mirage.jpg', 'mirage_2.png', 'mirage_3.png', 'Mirage',
 'Recreación de Mirage, uno de los mapas más emblemáticos de Counter-Strike: Global Offensive. Ambientado en una ciudad del norte de África, el escenario combina callejones estrechos, plazas abiertas y múltiples rutas de acceso entre sectores clave. Su diseño equilibrado favorece el juego táctico, el control de posiciones y la coordinación entre equipos en modalidades competitivas.',
 10,
 'Mirage es un clásico táctico por excelencia, inspirado en los callejones laberínticos y plazas del norte de África. Destaca por su diseño de tres vías con múltiples conexiones que exigen una excelente comunicación y control del mapa. Las zonas clave como el "Centro" (Mid) y los sitios de bomba proporcionan oportunidades tanto para asaltos directos como para estrategias de flanqueo. Requiere un enfoque coordinado, uso inteligente de coberturas y precisión para dominar sus ángulos y cuellos de botella.',
 'Instalaciones Kinetix - Sector Bravo',
 'Juego Táctico / Estrategia de equipo',
 'Urbano / Desértico',
 'Difícil',
 'Defuse (Buscar y Destruir) · Team Deathmatch · Dominio · Escolta VIP',
 'Counter-Strike: Global Offensive'),

-- HIJACKED
('hijacked.jpg', 'hijacked_2.png', 'hijacked_3.png', 'Hijacked',
 'Recreación de Hijacked, el icónico yate de lujo popularizado por Call of Duty: Black Ops II. Ambientado en una embarcación privada de alta gama en altamar, el escenario combina pasillos estrechos, cubiertas abiertas y múltiples niveles conectados. Su diseño compacto favorece enfrentamientos constantes, rápidas rotaciones y un ritmo de juego intenso en modalidades competitivas. Se lleva a cabo en Puerto Madero.',
 12,
 'Hijacked traslada la acción a las cubiertas de un espectacular superyate de lujo. El mapa cuenta con una distribución simétrica con dos estructuras principales en proa y popa conectadas por un área central abierta y pasillos laterales exteriores. Un conducto subterráneo en la sala de máquinas permite cruzar el barco de forma encubierta para sorprender por la espalda. Su escala compacta promueve tiroteos intensos en distancias cortas, reflejos inmediatos y batallas agresivas por el control de las plantas superiores.',
 'Puerto Madero - Dársena Norte',
 'Combate cerrado / Ritmo frenético',
 'Embarcación / Cubiertas y pasillos',
 'Media',
 'Team Deathmatch · Captura la Bandera · Dominio · Todos contra Todos',
 'Call of Duty: Black Ops II'),

-- TERMINAL
('terminal.jpg', 'terminal_2.png', 'terminal_3.png', 'Terminal',
 'Inspirado en Terminal de Call of Duty: Modern Warfare 3, este mapa recrea un aeropuerto internacional con terminales de pasajeros, corredores interiores y zonas de pista. Su diseño versátil favorece distintos estilos de juego y lo convierte en uno de los escenarios más versatiles para desarrollar todos los modos de juego. Se lleva a cabo el ex-aeropuerto de Don Torcuato.',
 14,
 'Terminal ofrece un escenario dinámico y multifacético que simula la terminal de un aeropuerto comercial a gran escala. Dividido entre un interior acristalado repleto de tiendas, controles de seguridad y pasillos estrechos, y una zona exterior en la pista de aterrizaje que incluye un avión civil completamente transitable. Su diseño equilibra las líneas de visión largas ideales para tiradores en la pista con cuellos de botella y coberturas densas en el interior, exigiendo adaptabilidad táctica constante.',
 'Ex-Aeródromo de Don Torcuato',
 'Juego versátil / Combate táctico',
 'Aeropuerto / Terminal y pista exterior',
 'Media',
 'Buscar y Destruir · Dominio · Team Deathmatch · Sabotaje',
 'Call of Duty: Modern Warfare 3');

INSERT IGNORE INTO Accounts (id, name, username, email, password, dni, phone, about_me, created_at, updated_at, is_active, is_admin)
VALUES (1, 'Juan Perez', 'juanperez', 'juanperez@email.com', '123456', '12345678', '123456789', 'Jugador de airsoft', NOW(), NOW(), TRUE, TRUE);


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
	name VARCHAR(75) CHARACTER SET utf8mb4 NOT NULL,
	duration ENUM('30', '60', '90', '120') NOT NULL,
	players INT NOT NULL,
	description TEXT,
	updated_at DATE
) DEFAULT CHARSET=utf8mb4;

INSERT IGNORE INTO GameModes (name, duration, players, description) VALUES
('Todos vs Todos', '60', 10, 'Todos los jugadores compiten por sí mismos. El último en pie o el que más eliminaciones consiga gana la partida.'),
('Captura la bandera', '90', 10, 'Dos equipos compiten por robar la bandera del equipo contrario y llevarla a su base. Coordinación y estrategia son clave.'),
('Duelo por equipos', '60', 10, 'Combate directo entre dos equipos. Gana el equipo que más bajas realice dentro del tiempo límite.'),
('Rey de la colina', '120', 20, 'Los equipos luchan por controlar una zona neutral. El equipo que mantenga la posición más tiempo acumulado gana.');

CREATE TABLE IF NOT EXISTS MapGameModes (
	map_id INT NOT NULL,
	gamemode_id INT NOT NULL,
	PRIMARY KEY (map_id, gamemode_id),
	FOREIGN KEY (map_id) REFERENCES Maps(id),
	FOREIGN KEY (gamemode_id) REFERENCES GameModes(id)
) DEFAULT CHARSET=utf8mb4;

INSERT IGNORE INTO MapGameModes (map_id, gamemode_id) VALUES
(1, 1), (1, 2), (1, 3),
(2, 1), (2, 3), (2, 4),
(3, 2), (3, 3), (3, 4),
(4, 1), (4, 2), (4, 3), (4, 4);
