CREATE DATABASE IF NOT EXISTS airsoftdb;

USE airsoftdb;

CREATE TABLE IF NOT EXISTS Accounts (
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	username VARCHAR(100) NOT NULL,
	email VARCHAR(100) UNIQUE NOT NULL,
	password VARCHAR(150) NOT NULL,
	dni VARCHAR(20) NOT NULL UNIQUE,
	gender VARCHAR(10),
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


CREATE TABLE IF NOT EXISTS EquipmentCategory (
    slug VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    title VARCHAR(200),
    subtitle TEXT,
    image_url VARCHAR(200),
    route_name VARCHAR(100) NOT NULL,
    sort_order INT DEFAULT 0
) DEFAULT CHARSET=utf8mb4;

INSERT IGNORE INTO EquipmentCategory (slug, name, title, subtitle, image_url, route_name, sort_order) VALUES
('arma', 'Armas', 'GUÍA DE USO Y TUTORIALES', 'Manuales e instructivos para el manejo seguro del equipamiento de airsoft.', 'img/arma.png', 'equipamiento_armas', 1),
('casco', 'Cascos y Accesorios', 'SISTEMAS DE PROTECCIÓN FACIAL', 'Blindaje avanzado y optimización de visibilidad. Indumentaria de seguridad certificada para operaciones en entornos de alta densidad de impactos.', 'img/casco.png', 'equipamiento_casco', 2),
('chaleco', 'Protección Personal', 'INDUMENTARIA DE COMBATE', 'Sistemas de blindaje corporal y vestimenta ergonómica optimizada para operaciones de alta intensidad. Seleccioná tu configuración de protección.', 'img/chaleco.png', 'equipamiento_chaleco', 3);

CREATE TABLE IF NOT EXISTS EquipmentKit (
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(200) CHARACTER SET utf8mb4 NOT NULL,
	category VARCHAR(50),
	brand VARCHAR(100),
	description TEXT CHARACTER SET utf8mb4,
	image_url VARCHAR(200),
	price FLOAT,
	quantity INT NOT NULL DEFAULT 1,
	purchase_link VARCHAR(500),
	details TEXT CHARACTER SET utf8mb4,
	sort_order INT DEFAULT 0
) DEFAULT CHARSET=utf8mb4;

INSERT IGNORE INTO EquipmentKit (id, name, category, brand, price, quantity) VALUES
(1, 'Kit Básico', NULL, 'Valken', 2000, 10);

INSERT IGNORE INTO EquipmentKit (id, name, category, brand, description, image_url, price, quantity, details, sort_order) VALUES
(4, 'Pistola Airsoft SW40F', 'arma', 'SW', 'BIENVENIDO AL MANUAL TÉCNICO AVANZADO ¡Sentí la experiencia táctica y llevá tus partidas al siguiente nivel! La SW40F es una pistola de juguete estilo airsoft con diseño realista, ideal para juego recreativo, colección o práctica de puntería.', 'img/pistola.png', 0, 5, '{"instructions":[{"title":"Carga y preparación","text":"Para comenzar, colocá las balas plásticas dentro del cargador incluido y asegurate de insertarlo correctamente en la pistola hasta escuchar el ajuste. El diseño del cargador permite una carga rápida y cómoda para continuar la diversión sin interrupciones."},{"title":"Activación del sistema de disparo","text":"Deslizá la corredera hacia atrás para comprimir el resorte interno y preparar el mecanismo. Este sistema manual estilo airsoft brinda una experiencia más realista y entretenida, simulando el funcionamiento de una pistola táctica recreativa."},{"title":"Disparo y uso recreativo","text":"Una vez preparado el mecanismo, simplemente presioná el gatillo para liberar la tensión del resorte y expulsar la bala plástica. Gracias a su diseño liviano y ergonómico, ofrece un agarre cómodo y fácil manejo para juegos recreativos, práctica de puntería o colección."}]}', 1),
(5, 'Rifle Airsoft 221A+ a Resorte Calibre 6MM', 'arma', NULL, 'Fabricado en polímero ABS de alto impacto, este rifle ofrece una estructura liviana, resistente y cómoda de manipular. Cuenta con corredera móvil, cargador estilo real y sistema monotiro que replica de manera muy fiel el funcionamiento de un rifle táctico real. Además, incorpora mira de puntería y una potencia aproximada de 340 FPS, ideal para prácticas de tiro recreativo y simulaciones.', 'img/rifle.png', 0, 5, '{"instructions":[{"title":"Carga del cargador","text":"Colocá los balines plásticos de 6 mm dentro del cargador y asegurate de insertarlo correctamente en el rifle hasta escuchar el ajuste. El sistema de cargador desmontable facilita una carga rápida y cómoda para continuar la experiencia sin interrupciones."},{"title":"Activación del mecanismo a resorte","text":"Deslizá la corredera para comprimir el resorte interno y preparar el sistema de disparo. Este mecanismo manual tipo monotiro brinda una experiencia más realista, simulando el funcionamiento de un rifle táctico recreativo."},{"title":"Disparo y uso recreativo","text":"Una vez preparado el mecanismo, presioná el gatillo para liberar la tensión del resorte y disparar el balín plástico. Gracias a su diseño ergonómico y liviano, el rifle ofrece un manejo cómodo para prácticas de puntería, simulaciones recreativas y colección táctica."}]}', 2),
(6, 'Remera Táctica Manga Larga Bajo Chaleco – Alpha Force', 'chaleco', NULL, 'La Remera Táctica Bajo Chaleco Alpha Force está diseñada para brindar comodidad, resistencia y libertad de movimiento en actividades tácticas y al aire libre. Su diseño de manga larga, cuello alto y corte ergonómico ofrece una apariencia profesional y un ajuste cómodo durante jornadas prolongadas de uso. Su construcción permite utilizarla cómodamente debajo de chalecos tácticos o como prenda principal, proporcionando una excelente movilidad sin sacrificar resistencia.', 'img/remera.png', 0, 5, '{"tag":"Ergonomía & Movilidad","specs":[{"label":"Material Exterior","value":"Fabricada con una combinación de algodón y tejido Ripstop de alta resistencia. Esta construcción proporciona comodidad, transpirabilidad y una excelente durabilidad frente al uso intensivo y las exigencias de actividades tácticas y outdoor."},{"label":"Diseño funcional","value":"Su diseño está pensado para utilizarse cómodamente bajo chalecos tácticos, ofreciendo confort durante largos períodos de uso sin perder una apariencia profesional."},{"label":"Ajuste de Talla","value":"Disponible en talles S, M, L, XL, XXL y XXXL. Su diseño se adapta a diferentes contexturas físicas, brindando un ajuste cómodo y seguro para acompañar cada movimiento durante la actividad."}]}', 1),
(7, 'Chaleco Táctico Protector', 'chaleco', NULL, 'Chaleco táctico multifunción diseñado para actividades recreativas y outdoor como airsoft, paintball, entrenamiento táctico y aventuras al aire libre. Su diseño moderno y ergonómico brinda una excelente combinación entre comodidad, resistencia y estilo profesional. Incluye 3 portacargadores frontales con cierre de seguridad, ideales para transportar accesorios esenciales de manera práctica y segura. Además, incorpora una zona frontal con velcro compatible con parches tácticos y accesorios modulares para personalizar el equipo según las necesidades del usuario.', 'img/chaleco.png', 0, 5, '{"tag":"Protección Superior","specs":[{"label":"Material exterior","value":"Fabricado en nailon 600D de alta calidad, un material reconocido por su gran resistencia al desgaste, impactos y uso intensivo."},{"label":"Sistema de anclaje","value":"Cuenta con sistema modular frontal con velcro y portacargadores integrados con cierre de seguridad, permitiendo transportar accesorios tácticos de manera organizada, cómoda y segura."},{"label":"Talla y ajuste","value":"Diseño totalmente ajustable en hombros y cintura para adaptarse cómodamente a distintas contexturas físicas. Su estructura ergonómica proporciona un ajuste firme, cómodo y estable durante el movimiento."}]}', 2),
(8, 'Protector Inguinal Táctico', 'chaleco', NULL, 'El Protector Inguinal Táctico MOLLE está diseñado para complementar chalecos tácticos con una solución práctica, cómoda y de aspecto profesional. Su diseño permite incorporar placas de protección flexibles y rígidas compatibles, brindando una configuración más completa para equipamiento táctico y recreativo.', 'img/ingle.png', 0, 5, '{"tag":"Protección Inferior","specs":[{"label":"Material exterior","value":"Confeccionado en tela Cordura importada 600D de alta resistencia, combinada con correas reforzadas de polipropileno para ofrecer durabilidad y un excelente rendimiento durante el uso intensivo."},{"label":"Sistema de anclaje","value":"Cuenta con sistema modular frontal con velcro y portacargadores integrados con cierre de seguridad, permitiendo transportar accesorios tácticos de manera organizada, cómoda y segura."},{"label":"Talla y ajuste","value":"Sus correas regulables permiten ajustar la posición para obtener una sujeción cómoda, firme y segura según las preferencias de cada usuario."}]}', 3),
(9, 'Pantalón Táctico Outdoor', 'chaleco', NULL, 'El Pantalón Outdoor Premium está diseñado para quienes buscan comodidad, resistencia y funcionalidad en cada actividad. Su diseño moderno y ergonómico permite una excelente libertad de movimiento, convirtiéndolo en una opción ideal para actividades tácticas, airsoft, entrenamiento y aventuras al aire libre.', 'img/pantalon.png', 0, 5, '{"tag":"Protección Inferior","specs":[{"label":"Material exterior","value":"Confeccionado en nylon de alta calidad, un material reconocido por su excelente resistencia al desgaste, gran durabilidad y propiedades impermeables. Además, incorpora cierres YKK de alto rendimiento, diseñados para soportar un uso intensivo en distintas condiciones."},{"label":"Sistema de anclaje","value":"Cuenta con regulaciones en cintura y botamanga que permiten personalizar el ajuste según las preferencias del usuario."},{"label":"Talla y ajuste","value":"Diseñado para ofrecer un ajuste cómodo y seguro durante largas jornadas de uso. Incluye forro térmico desmontable para adaptarse a diferentes condiciones climáticas y cierres de ventilación que favorecen una adecuada circulación del aire."}]}', 4),
(10, 'Casco Táctico Ajustable', 'casco', NULL, 'El Casco Táctico Militar Fast está diseñado para quienes buscan complementar su equipamiento con un accesorio funcional, cómodo y de apariencia profesional. Su diseño táctico moderno ofrece una excelente combinación entre estética y practicidad, siendo ideal para airsoft, entrenamiento recreativo y actividades al aire libre.', 'img/casco2.png', 0, 5, '{"sku":"SATORI-FAST","status":"HOMOLOGADO","stats":[{"label":"ABSORCIÓN DE IMPACTO","percentage":95},{"label":"ERGONOMÍA CRANEAL","percentage":80}]}', 1),
(11, 'Antiparras Balísticas Alpha', 'casco', NULL, 'Protección ocular absoluta con certificación balística EN166. El marco perimetral de goma sellada suprime los ángulos ciegos contra impactos externos. Integra tecnología micro-estriada de ventilación activa y capas químicas anti-fog que mitigan el empañamiento por transpiración.', 'img/gafas.png', 0, 5, '{"sku":"SPECTER-V2","status":"CRÍTICO","stats":[{"label":"PROTECCIÓN BALÍSTICA","percentage":100},{"label":"SISTEMA ANTI-EMPAÑANTE","percentage":90}]}', 2),
(12, 'Balaclava Táctica Ergonómica', 'casco', NULL, 'Capa de aislamiento confeccionada en tejido elástico transpirable (híbrido poliéster/spandex). Protege el cuello y el contorno mandibular contra quemaduras por fricción e impactos menores, actuando además como barrera higiénica absorbente bajo el casco rígido.', 'img/pasamontaña.png', 0, 5, '{"sku":"SHIELD-DRY","status":"COMPLEMENTO","stats":[{"label":"TRANSPIRABILIDAD","percentage":95},{"label":"PROTECCIÓN TÉRMICA","percentage":60}]}', 3);


CREATE TABLE IF NOT EXISTS Maps (
	id INT AUTO_INCREMENT PRIMARY KEY,
	image_url VARCHAR(100),
	name VARCHAR(100) CHARACTER SET utf8mb4 UNIQUE,
	description VARCHAR(900) CHARACTER SET utf8mb4

) DEFAULT CHARSET=utf8mb4;

INSERT IGNORE INTO Maps (name, description) VALUES
('Nuketown', 'Mapa clásico de combate urbano'),
('Mirage', 'Mapa táctico con zonas desérticas'),
('Hijacked', 'Mapa ambientado en un yate de lujo'),
('Terminal', 'Mapa ambientado en un aeropuerto');

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
