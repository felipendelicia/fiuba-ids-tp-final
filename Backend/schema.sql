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
('arma', 'Armas', 'GUIA DE USO Y TUTORIALES', 'Manuales e instructivos para el manejo seguro del equipamiento de airsoft.', 'img/arma.png', 'equipamiento_armas', 1),
('casco', 'Cascos y Accesorios', 'SISTEMAS DE PROTECCION FACIAL', 'Blindaje avanzado y optimizacion de visibilidad. Indumentaria de seguridad certificada para operaciones en entornos de alta densidad de impactos.', 'img/casco.png', 'equipamiento_casco', 2),
('chaleco', 'Proteccion Personal', 'INDUMENTARIA DE COMBATE', 'Sistemas de blindaje corporal y vestimenta ergonomica optimizada para operaciones de alta intensidad. Selecciona tu configuracion de proteccion.', 'img/chaleco.png', 'equipamiento_chaleco', 3);

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
(1, 'Kit Basico', NULL, 'Valken', 2000, 10);

INSERT IGNORE INTO EquipmentKit (id, name, category, brand, description, image_url, price, quantity, details, sort_order) VALUES
(4, 'Pistola Airsoft SW40F', 'arma', 'SW', 'BIENVENIDO AL MANUAL TECNICO AVANZADO ¡Senti la experiencia tactica y lleva tus partidas al siguiente nivel! La SW40F es una pistola de juguete estilo airsoft con diseño realista, ideal para juego recreativo, coleccion o practica de punteria.', 'img/pistola.png', 15000, 5, '{"instructions":[{"title":"Carga y preparacion","text":"Para comenzar, coloca las balas plasticas dentro del cargador incluido y asegurate de insertarlo correctamente en la pistola hasta escuchar el ajuste. El diseño del cargador permite una carga rapida y comoda para continuar la diversion sin interrupciones."},{"title":"Activacion del sistema de disparo","text":"Desliza la corredera hacia atras para comprimir el resorte interno y preparar el mecanismo. Este sistema manual estilo airsoft brinda una experiencia mas realista y entretenida, simulando el funcionamiento de una pistola tactica recreativa."},{"title":"Disparo y uso recreativo","text":"Una vez preparado el mecanismo, simplemente presiona el gatillo para liberar la tension del resorte y expulsar la bala plastica. Gracias a su diseño liviano y ergonomico, ofrece un agarre comodo y facil manejo para juegos recreativos, practica de punteria o coleccion."}]}', 1),
(5, 'Rifle Airsoft 221A+ a Resorte Calibre 6MM', 'arma', NULL, 'Fabricado en polimero ABS de alto impacto, este rifle ofrece una estructura liviana, resistente y comoda de manipular. Cuenta con corredera movil, cargador estilo real y sistema monotiro que replica de manera muy fiel el funcionamiento de un rifle tactico real. Ademas, incorpora mira de punteria y una potencia aproximada de 340 FPS, ideal para practicas de tiro recreativo y simulaciones.', 'img/rifle.png', 25000, 5, '{"instructions":[{"title":"Carga del cargador","text":"Coloca los balines plasticos de 6 mm dentro del cargador y asegurate de insertarlo correctamente en el rifle hasta escuchar el ajuste. El sistema de cargador desmontable facilita una carga rapida y comoda para continuar la experiencia sin interrupciones."},{"title":"Activacion del mecanismo a resorte","text":"Desliza la corredera para comprimir el resorte interno y preparar el sistema de disparo. Este mecanismo manual tipo monotiro brinda una experiencia mas realista, simulando el funcionamiento de un rifle tactico recreativo."},{"title":"Disparo y uso recreativo","text":"Una vez preparado el mecanismo, presiona el gatillo para liberar la tension del resorte y disparar el balin plastico. Gracias a su diseño ergonomico y liviano, el rifle ofrece un manejo comodo para practicas de punteria, simulaciones recreativas y coleccion tactica."}]}', 2),
(6, 'Remera Tactica Manga Larga Bajo Chaleco – Alpha Force', 'chaleco', NULL, 'La Remera Tactica Bajo Chaleco Alpha Force esta diseñada para brindar comodidad, resistencia y libertad de movimiento en actividades tacticas y al aire libre. Su diseño de manga larga, cuello alto y corte ergonomico ofrece una apariencia profesional y un ajuste comodo durante jornadas prolongadas de uso. Su construccion permite utilizarla comodamente debajo de chalecos tacticos o como prenda principal, proporcionando una excelente movilidad sin sacrificar resistencia.', 'img/remera.png', 8000, 5, '{"tag":"Ergonomia & Movilidad","specs":[{"label":"Material Exterior","value":"Fabricada con una combinacion de algodon y tejido Ripstop de alta resistencia. Esta construccion proporciona comodidad, transpirabilidad y una excelente durabilidad frente al uso intensivo y las exigencias de actividades tacticas y outdoor."},{"label":"Diseño funcional","value":"Su diseño esta pensado para utilizarse comodamente bajo chalecos tacticos, ofreciendo confort durante largos periodos de uso sin perder una apariencia profesional."},{"label":"Ajuste de Talla","value":"Disponible en talles S, M, L, XL, XXL y XXXL. Su diseño se adapta a diferentes contexturas fisicas, brindando un ajuste comodo y seguro para acompañar cada movimiento durante la actividad."}]}', 1),
(7, 'Chaleco Tactico Protector', 'chaleco', NULL, 'Chaleco tactico multifuncion diseñado para actividades recreativas y outdoor como airsoft, paintball, entrenamiento tactico y aventuras al aire libre. Su diseño moderno y ergonomico brinda una excelente combinacion entre comodidad, resistencia y estilo profesional. Incluye 3 portacargadores frontales con cierre de seguridad, ideales para transportar accesorios esenciales de manera practica y segura. Ademas, incorpora una zona frontal con velcro compatible con parches tacticos y accesorios modulares para personalizar el equipo segun las necesidades del usuario.', 'img/chaleco.png', 18000, 5, '{"tag":"Proteccion Superior","specs":[{"label":"Material exterior","value":"Fabricado en nailon 600D de alta calidad, un material reconocido por su gran resistencia al desgaste, impactos y uso intensivo."},{"label":"Sistema de anclaje","value":"Cuenta con sistema modular frontal con velcro y portacargadores integrados con cierre de seguridad, permitiendo transportar accesorios tacticos de manera organizada, comoda y segura."},{"label":"Talla y ajuste","value":"Diseño totalmente ajustable en hombros y cintura para adaptarse comodamente a distintas contexturas fisicas. Su estructura ergonomica proporciona un ajuste firme, comodo y estable durante el movimiento."}]}', 2),
(8, 'Protector Inguinal Tactico', 'chaleco', NULL, 'El Protector Inguinal Tactico MOLLE esta diseñado para complementar chalecos tacticos con una solucion practica, comoda y de aspecto profesional. Su diseño permite incorporar placas de proteccion flexibles y rigidas compatibles, brindando una configuracion mas completa para equipamiento tactico y recreativo.', 'img/ingle.png', 6000, 5, '{"tag":"Proteccion Inferior","specs":[{"label":"Material exterior","value":"Confeccionado en tela Cordura importada 600D de alta resistencia, combinada con correas reforzadas de polipropileno para ofrecer durabilidad y un excelente rendimiento durante el uso intensivo."},{"label":"Sistema de anclaje","value":"Cuenta con sistema modular frontal con velcro y portacargadores integrados con cierre de seguridad, permitiendo transportar accesorios tacticos de manera organizada, comoda y segura."},{"label":"Talla y ajuste","value":"Sus correas regulables permiten ajustar la posicion para obtener una sujecion comoda, firme y segura segun las preferencias de cada usuario."}]}', 3),
(9, 'Pantalon Tactico Outdoor', 'chaleco', NULL, 'El Pantalon Outdoor Premium esta diseñado para quienes buscan comodidad, resistencia y funcionalidad en cada actividad. Su diseño moderno y ergonomico permite una excelente libertad de movimiento, convirtiendolo en una opcion ideal para actividades tacticas, airsoft, entrenamiento y aventuras al aire libre.', 'img/pantalon.png', 12000, 5, '{"tag":"Proteccion Inferior","specs":[{"label":"Material exterior","value":"Confeccionado en nylon de alta calidad, un material reconocido por su excelente resistencia al desgaste, gran durabilidad y propiedades impermeables. Ademas, incorpora cierres YKK de alto rendimiento, diseñados para soportar un uso intensivo en distintas condiciones."},{"label":"Sistema de anclaje","value":"Cuenta con regulaciones en cintura y botamanga que permiten personalizar el ajuste segun las preferencias del usuario."},{"label":"Talla y ajuste","value":"Diseñado para ofrecer un ajuste comodo y seguro durante largas jornadas de uso. Incluye forro termico desmontable para adaptarse a diferentes condiciones climaticas y cierres de ventilacion que facilitan una adecuada circulacion del aire."}]}', 4),
(10, 'Casco Tactico Ajustable', 'casco', NULL, 'El Casco Tactico Militar Fast esta diseñado para quienes buscan complementar su equipamiento con un accesorio funcional, comodo y de apariencia profesional. Su diseño tactico moderno ofrece una excelente combinacion entre estetica y practicidad, siendo ideal para airsoft, entrenamiento recreativo y actividades al aire libre.', 'img/casco2.png', 10000, 5, '{"sku":"SATORI-FAST","status":"HOMOLOGADO","stats":[{"label":"ABSORCION DE IMPACTO","percentage":95},{"label":"ERGONOMIA CRANEAL","percentage":80}]}', 1),
(11, 'Antiparras Balisticas Alpha', 'casco', NULL, 'Proteccion ocular absoluta con certificacion balistica EN166. El marco perimetral de goma sellada suprime los angulos ciegos contra impactos externos. Integra tecnologia micro-estriada de ventilacion activa y capas quimicas anti-fog que mitigan el empañamiento por transpiracion.', 'img/gafas.png', 7000, 5, '{"sku":"SPECTER-V2","status":"CRITICO","stats":[{"label":"PROTECCION BALISTICA","percentage":100},{"label":"SISTEMA ANTI-EMPAÑANTE","percentage":90}]}', 2),
(12, 'Balaclava Tactica Ergonomica', 'casco', NULL, 'Capa de aislamiento confeccionada en tejido elastico transpirable (hibrido poliester/spandex). Protege el cuello y el contorno mandibular contra quemaduras por friccion e impactos menores, actuando ademas como barrera higienica absorbente bajo el casco rigido.', 'img/pasamontaña.png', 4000, 5, '{"sku":"SHIELD-DRY","status":"COMPLEMENTO","stats":[{"label":"TRANSPIRABILIDAD","percentage":95},{"label":"PROTECCION TERMICA","percentage":60}]}', 3);

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
    difficulty ENUM('Facil', 'Media', 'Dificil'),
    compatible_gamemodes VARCHAR(300),
    origin VARCHAR(100),
    plano_image_url VARCHAR(100),
    zone_1_name VARCHAR(100),
    zone_1_description VARCHAR(300),
    zone_2_name VARCHAR(100),
    zone_2_description VARCHAR(300),
    zone_3_name VARCHAR(100),
    zone_3_description VARCHAR(300)
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
    origin,
    plano_image_url,
    zone_1_name,
    zone_1_description,
    zone_2_name,
    zone_2_description,
    zone_3_name,
    zone_3_description
) VALUES
-- NUKETOWN
('nuketown.jpg', 'nuketown_2.png', 'nuketown_3.png', 'Nuketown',
 'Recreacion de Nuketown 2025, el clasico escenario futurista popularizado por Call of Duty: Black Ops II. Inspirado en un vecindario construido para ensayos y demostraciones dentro de una instalacion de pruebas nucleares, ofrece una distribucion equilibrada que favorece partidas rapidas y enfrentamientos constantes entre ambos equipos.',
 10,
 'Nuketown 2025 es una recreacion a escala real del famoso mapa de Call of Duty: Black Ops II. Ambientado en un vecindario suburbano construido dentro de una instalacion de pruebas nucleares, ofrece un campo de batalla simetrico y equilibrado. Las dos casas enfrentadas, los vehiculos en el frente y los patios traseros conforman el nucleo del combate. Su diseño promueve enfrentamientos rapidos, reflejos afilados y accion constante. Ideal para partidas casuales y torneos cortos donde la velocidad de reaccion define al vencedor.',
 'Instalaciones Kinetix - Sector Alpha',
 'Combate rapido / Accion constante',
 'Urbano / Calles y edificios',
 'Media',
 'Team Deathmatch · Dominio · Captura la Bandera · Todos contra Todos',
 'Call of Duty: Black Ops II',
 'plano_nuketown.png',
 'Acceso principal y zona de bienvenida', 'Entrada principal al complejo, diseñada para recibir a los visitantes y brindar una vista general del proyecto. Incluye el area de estacionamiento, senderos peatonales, señaletica tematica de Nuketown y espacios de circulacion que conectan con el resto de las instalaciones.',
 'Plaza central y area recreativa', 'Nucleo central del mapa compuesto por espacios verdes, arboles ornamentales, banderas decorativas y zonas de descanso. La via circular que la rodea facilita el recorrido de vehiculos y peatones, convirtiendola en el principal punto de encuentro y distribucion del complejo.',
 'Zonas especiales y estructuras futuristas', 'Sector destinado a las construcciones mas representativas del proyecto, incluyendo el Domo de la Biosfera y otras estructuras de diseño futurista. Estas instalaciones aportan identidad visual al mapa y funcionan como puntos de interes arquitectonico y recreativo para los visitantes.'),

-- MIRAGE
('mirage.jpg', 'mirage_2.png', 'mirage_3.png', 'Mirage',
 'Recreacion de Mirage, uno de los mapas mas emblematicos de Counter-Strike: Global Offensive. Ambientado en una ciudad del norte de Africa, el escenario combina callejones estrechos, plazas abiertas y multiples rutas de acceso entre sectores clave. Su diseño equilibrado favorece el juego tactico, el control de posiciones y la coordinacion entre equipos en modalidades competitivas.',
 10,
 'Mirage es un clasico tactico por excelencia, inspirado en los callejones laberinticos y plazas del norte de Africa. Destaca por su diseño de tres vias con multiples conexiones que exigen una excelente comunicacion y control del mapa. Las zonas clave como el "Centro" (Mid) y los sitios de bomba proporcionan oportunidades tanto para asaltos directos como para estrategias de flanqueo. Requiere un enfoque coordinado, uso inteligente de coberturas y precision para dominar sus angulos y cuellos de botella.',
 'Instalaciones Kinetix - Sector Bravo',
 'Juego Tactico / Estrategia de equipo',
 'Urbano / Desertico',
 'Dificil',
 'Defuse (Buscar y Destruir) · Team Deathmatch · Dominio · Escolta VIP',
 'Counter-Strike: Global Offensive',
 'plano_mirage.png',
 'Zona de Contencion y Logistica Terrestre', 'Esta gran seccion abarca toda la franja norte y noroeste del predio, donde se ubican el almacen de equipamiento de 15 m X 10 m y las pilas de municiones pesadas. Esta diseñada estructuralmente como una barrera perimetral masiva que delimita el fondo del escenario.',
 'El Nucleo de Fuego y Conflicto Directo', 'Es el corazon del mapa, dominado por el simbolo central de grafiti y la gran plataforma de cajas de carga apiladas. Al ser una explanada completamente despejada con pavimento rigido, se convierte de inmediato en el epicentro de maxima exposicion y peligro.',
 'Zona de Descompresion', 'Situada en el lateral este del plano, esta franja destaca por su cambio de suelo hacia la arena, fuentes de agua y vegetacion de palmeras altas. Visualmente actua como un respiro estetico (oasis), pero operativamente funciona como el callejon de flanqueo mas peligroso del entorno.'),

-- HIJACKED
('hijacked.jpg', 'hijacked_2.png', 'hijacked_3.png', 'Hijacked',
 'Recreacion de Hijacked, el iconico yate de lujo popularizado por Call of Duty: Black Ops II. Ambientado en una embarcacion privada de alta gama en altamar, el escenario combina pasillos estrechos, cubiertas abiertas y multiples niveles conectados. Su diseño compacto favorece enfrentamientos constantes, rapidas rotaciones y un ritmo de juego intenso en modalidades competitivas. Se lleva a cabo en Puerto Madero.',
 12,
 'Hijacked traslada la accion a las cubiertas de un espectacular superyate de lujo. El mapa cuenta con una distribucion simetrica con dos estructuras principales en proa y popa conectadas por un area central abierta y pasillos laterales exteriores. Un conducto subterraneo en la sala de maquinas permite cruzar el barco de forma encubierta para sorprender por la espalda. Su escala compacta promueve tiroteos intensos en distancias cortas, reflejos inmediatos y batallas agresivas por el control de las plantas superiores.',
 'Puerto Madero - Darsena Norte',
 'Combate cerrado / Ritmo frenetico',
 'Embarcacion / Cubiertas y pasillos',
 'Media',
 'Team Deathmatch · Captura la Bandera · Dominio · Todos contra Todos',
 'Call of Duty: Black Ops II',
 'plano_hijacked.png',
 'Zona de Acceso y Logistica', 'Esta seccion comprende la entrada principal desde la plataforma de baño trasera, el helipuerto y el salon comedor principal en el primer piso. Al ser el punto de partida y la zona de circulacion mas amplia, esta diseñada para un transito fluido y la recepcion del flujo de personas.',
 'Zona de Alta Intensidad y Conflicto Central', 'Ubicada en la parte media de la cubierta superior (segundo piso), esta area concentra el mayor atractivo visual y operativo. Al albergar la zona de solarium, el jacuzzi y los pasillos abiertos que conectan proa con popa, se convierte en el punto caliente del mapa donde se cruzan todos los recorridos.',
 'Puntos Estrategicos de Comando', 'Esta categoria engloba las posiciones elevadas y los extremos cerrados del yate: el puente de mando principal al frente y el salon VIP/Sky Lounge en la zona alta. Son sectores clave para dominar la estrategia del mapa, ya que ofrecen una ventaja tactica de altura y control visual sobre las cubiertas inferiores.'),

-- TERMINAL
('terminal.jpg', 'terminal_2.png', 'terminal_3.png', 'Terminal',
 'Inspirado en Terminal de Call of Duty: Modern Warfare 3, este mapa recrea un aeropuerto internacional con terminales de pasajeros, corredores interiores y zonas de pista. Su diseño versatil favorece distintos estilos de juego y lo convierte en uno de los escenarios mas versatiles para desarrollar todos los modos de juego. Se lleva a cabo el ex-aeropuerto de Don Torcuato.',
 14,
 'Terminal ofrece un escenario dinamico y multifacetico que simula la terminal de un aeropuerto comercial a gran escala. Dividido entre un interior acristalado repleto de tiendas, controles de seguridad y pasillos estrechos, y una zona exterior en la pista de aterrizaje que incluye un avion civil completamente transitable. Su diseño equilibra las lineas de vision largas ideales para tiradores en la pista con cuellos de botella y coberturas densas en el interior, exigiendo adaptabilidad tactica constante.',
 'Ex-Aerodromo de Don Torcuato',
 'Juego versatil / Combate tactico',
 'Aeropuerto / Terminal y pista exterior',
 'Media',
 'Buscar y Destruir · Dominio · Team Deathmatch · Sabotaje',
 'Call of Duty: Modern Warfare 3',
 'plano_terminal.png',
 'Zona de Impacto', 'Es el sector exterior mas masivo del mapa, dominado por un avion de 28.7 m de envergadura y una pista asfaltada de 21.5 m de largo. Una zona completamente abierta, ideal para transiciones rapidas entre las cajas de carga y los vehiculos policiales.',
 'Nucleo Operativo', 'El corazon del aeropuerto que conecta la entrada principal con los mostradores de recepcion y el control de escaneres. Es un laberinto interior con pasillos de 1.18 m de ancho y oficinas comerciales que obligan al combate a corta distancia y al control de esquinas ciegas.',
 'Punto Caliente', 'La zona este del mapa, un cuello de botella critico que concentra las salas de espera, asientos y el famoso local de comidas. Al tener accesos reducidos de 1.2 m a 1.9 m, es el sector de maxima friccion defensiva donde se definen las partidas.');


CREATE TABLE IF NOT EXISTS GameModes (
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(75) CHARACTER SET utf8mb4 NOT NULL,
	duration ENUM('30', '60', '90', '120') NOT NULL,
	players INT NOT NULL,
	description TEXT,
	updated_at DATE
) DEFAULT CHARSET=utf8mb4;

INSERT IGNORE INTO GameModes (name, duration, players, description) VALUES
('Todos vs Todos', '120', 10, 'Todos los jugadores compiten por si mismos. El ultimo en pie o el que mas eliminaciones consiga gana la partida.'),
('Captura la bandera', '120', 10, 'Dos equipos compiten por robar la bandera del equipo contrario y llevarla a su base. Coordinacion y estrategia son clave.'),
('Duelo por equipos', '120', 10, 'Combate directo entre dos equipos. Gana el equipo que mas bajas realice dentro del tiempo limite.'),
('Rey de la colina', '120', 20, 'Los equipos luchan por controlar una zona neutral. El equipo que mantenga la posicion mas tiempo acumulado gana.');

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

CREATE TABLE IF NOT EXISTS Salas (
	id INT AUTO_INCREMENT PRIMARY KEY,
	game_mode_id INT NOT NULL,
	map_id INT NOT NULL,
	equipment_kit_id INT,
	price INT NOT NULL,
	reservation_date DATE NOT NULL,
	start_time TIME NOT NULL,
	end_time TIME NOT NULL,
	max_players INT NOT NULL DEFAULT 4,
	admin_account_id INT NOT NULL,
	is_public BOOLEAN DEFAULT TRUE,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	canceled BOOLEAN DEFAULT FALSE,
	cancelation_reason VARCHAR(500),
	FOREIGN KEY (game_mode_id) REFERENCES GameModes(id),
	FOREIGN KEY (map_id) REFERENCES Maps(id),
	FOREIGN KEY (equipment_kit_id) REFERENCES EquipmentKit(id),
	FOREIGN KEY (admin_account_id) REFERENCES Accounts(id),
	CHECK (
		canceled = TRUE OR (
			HOUR(start_time) IN (5,7,9,11,13,15,17,19)
			AND end_time = ADDTIME(start_time, '02:00:00')
		)
	)
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS Reservations (
	id INT AUTO_INCREMENT PRIMARY KEY,
	sala_id INT NOT NULL,
	account_id INT NOT NULL,
	equipment_kit_id INT NOT NULL,
	price INT NOT NULL,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	canceled BOOLEAN DEFAULT FALSE,
	FOREIGN KEY (sala_id) REFERENCES Salas(id),
	FOREIGN KEY (account_id) REFERENCES Accounts(id),
	FOREIGN KEY (equipment_kit_id) REFERENCES EquipmentKit(id),
	UNIQUE KEY uq_account_sala (account_id, sala_id)
) DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS RegisteredPlayers (
	id INT AUTO_INCREMENT PRIMARY KEY,
	reservation_id INT NOT NULL,
	account_id INT NOT NULL,
	created_at DATE
);

INSERT IGNORE INTO Accounts (id, name, username, email, password, dni, phone, about_me, created_at, updated_at, is_active, is_admin)
VALUES (1, 'Juan Perez', 'juanperez', 'juanperez@email.com', '123456', '12345678', '123456789', 'Jugador de airsoft', NOW(), NOW(), TRUE, TRUE);

CREATE TABLE IF NOT EXISTS Review (
	id INT AUTO_INCREMENT PRIMARY KEY,
	stars INT NOT NULL CHECK (stars BETWEEN 1 AND 5),
	title VARCHAR(200),
	body_review VARCHAR(900),
	map_id INT NOT NULL,
	created_at DATE,
	approved BOOLEAN,
	admin_response TEXT
);

CREATE TABLE IF NOT EXISTS CompetitivoEvent (
	id INT AUTO_INCREMENT PRIMARY KEY,
	title VARCHAR(200) NOT NULL,
	description TEXT,
	image_url VARCHAR(200),
	badge VARCHAR(50),
	event_date VARCHAR(100),
	event_time VARCHAR(100),
	sort_order INT DEFAULT 0
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS NosotrosInfo (
	section VARCHAR(50) PRIMARY KEY,
	title VARCHAR(200),
	subtitle VARCHAR(200),
	paragraphs TEXT
) DEFAULT CHARSET=utf8mb4;

INSERT IGNORE INTO NosotrosInfo (section, title, subtitle, paragraphs) VALUES
('main', 'Sobre Nosotros', 'Desde 2020', '["<span class=\"nosotros__highlight\">Kinetix</span> nace de la pasion por el airsoft tactico y la necesidad de crear un espacio donde la estrategia, el trabajo en equipo y la adrenalina se combinen en experiencias unicas. Somos un centro de recreacion y entrenamiento ubicado en <span class=\"nosotros__highlight\">Jose C. Paz</span>, diseñado tanto para jugadores principiantes como para veteranos del campo de batalla.", "Cada uno de nuestros campos —<span class=\"nosotros__highlight\">Nuketown</span>, <span class=\"nosotros__highlight\">Mirage</span>, <span class=\"nosotros__highlight\">Hijacked</span> y <span class=\"nosotros__highlight\">Terminal</span>— esta inspirado en escenarios iconicos de videojuegos y recreado a escala real para ofrecer una inmersion total. Desde calles urbanas hasta un yate de lujo en Puerto Madero, cada partida es una nueva mision.", "Contamos con equipamiento profesional, sistema de marcacion de impactos en tiempo real, chalecos tacticos, replicas de alta calidad y un bufet para la recarga de energia entre combates. Nuestro objetivo es que cada visitante viva el airsoft como nunca antes."]');

CREATE TABLE IF NOT EXISTS NosotrosCard (
	id INT AUTO_INCREMENT PRIMARY KEY,
	icon_class VARCHAR(100) NOT NULL,
	title VARCHAR(100) NOT NULL,
	description TEXT NOT NULL,
	sort_order INT DEFAULT 0
) DEFAULT CHARSET=utf8mb4;

INSERT IGNORE INTO NosotrosCard (id, icon_class, title, description, sort_order) VALUES
(1, 'fa-solid fa-crosshairs', 'Mision', 'Ofrecer la experiencia de airsoft mas realista y emocionante de la region, fomentando el compañerismo y la estrategia.', 1),
(2, 'fa-solid fa-eye', 'Vision', 'Ser el centro de airsoft de referencia en Argentina, con campos tematicos y tecnologia de punta.', 2),
(3, 'fa-solid fa-shield-halved', 'Valores', 'Seguridad, respeto, trabajo en equipo, innovacion constante y pasion por el deporte tactico.', 3),
(4, 'fa-solid fa-location-dot', 'Ubicacion', 'Jose C. Paz, Provincia de Buenos Aires. Facil acceso y estacionamiento para todo el equipo.', 4);

CREATE TABLE IF NOT EXISTS ContactMessage (
	id INT AUTO_INCREMENT PRIMARY KEY,
	user_name VARCHAR(100) NOT NULL,
	email VARCHAR(150) NOT NULL,
	message TEXT NOT NULL,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	leido TINYINT DEFAULT 0
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS Service (
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	tab_icon VARCHAR(50) DEFAULT 'bi bi-gear',
	summary_title VARCHAR(200),
	summary_text TEXT,
	bullet_1 TEXT,
	bullet_2 TEXT,
	tab_image VARCHAR(300),
	detail_title VARCHAR(200),
	detail_subtitle TEXT,
	section_1_title VARCHAR(200),
	section_1_text TEXT,
	section_2_title VARCHAR(200),
	section_2_text TEXT,
	detail_image_1 VARCHAR(300),
	detail_image_2 VARCHAR(300),
	breadcrumb_label VARCHAR(100),
	sort_order INT DEFAULT 0
) DEFAULT CHARSET=utf8mb4;

INSERT IGNORE INTO Service (id, name, tab_icon, summary_title, summary_text, bullet_1, bullet_2, tab_image, detail_title, detail_subtitle, section_1_title, section_1_text, section_2_title, section_2_text, detail_image_1, detail_image_2, breadcrumb_label, sort_order) VALUES
(1, 'Buffet & Bar', 'bi bi-cup-hot', 'Buffet & Zona de Descanso', 'Contamos con una cantina completamente equipada para recargar energias entre partidas. Ofrecemos una amplia variedad de comidas rapidas, minutas, snacks y bebidas heladas.', 'Hamburguesas completas y opciones vegetarianas.', 'Bebidas hidratantes, energizantes y cafeteria completa.', 'img/bufet.png', 'BUFFET / BAR INFO COMPLETA', 'Nuestra zona gastronomica esta pensada para cubrir todas las necesidades del jugador de Airsoft antes, durante y despues de la simulacion militar.', 'Menu de Combate', 'Ofrecemos un menu rapido de alta calidad que incluye hamburguesas premium, sandwiches de milanesa, pizzas calientes y opciones aptas para celiacos y vegetarianos. Todo elaborado en el momento.', 'Hidratacion Estrategica', 'Un combatiente deshidratado pierde efectividad. Mantenemos stock constante de agua mineral, bebidas isotonicas, jugos naturales, energizantes y cafeteria completa para los dias frios.', 'img/bufet_2.png', 'img/bufet_3.png', 'Buffet', 1),
(2, 'Estacionamiento Privado', 'bi bi-p-circle', 'Estacionamiento Controlado', 'Tu tranquilidad es prioridad. Disponemos de un predio de estacionamiento privado dentro de las instalaciones del club, totalmente cerrado y vigilado mecanicamente.', 'Capacidad para mas de 80 vehiculos en simultaneo.', 'Camaras de seguridad de circuito cerrado las 24 hs.', 'img/estacionamiento.png', 'ESTACIONAMIENTO PRIVADO INFO', 'Deja tu vehiculo con total tranquilidad mientras te concentras al 100% en los objetivos tacticos dentro del campo de juego.', 'Seguridad Perimetral', 'El predio esta completamente delimitado con alambrado olimpico, cuenta con un unico porton de acceso controlado y un custodio fisico asignado durante los eventos masivos.', 'Monitoreo CCTV', 'Implementamos domos de seguridad con vision nocturna infrarroja conectados a nuestra central del predio, registrando de forma ininterrumpida patentes y movimientos.', 'img/estacionamiento_2.png', 'img/estacionamiento_3.png', 'Estacionamiento', 2),
(3, 'Almacenamiento / Lockers', 'bi bi-safe', 'Almacenamiento Seguro', 'Resguarda tu equipamiento tactico, replicas y objetos personales de valor mientras estas en combate. Contamos con un sector exclusivo de lockers individuales reforzados.', 'Lockers individuales con llaves codificadas.', 'Monitoreo constante por personal del predio.', 'img/almacenamiento.png', 'SISTEMA DE LOCKERS SEGUROS', 'Sabemos el valor de tus replicas y chalecos tacticos. Por eso creamos una zona exclusiva para el resguardo de tu material militar.', 'Asignacion Personalizada', 'Al realizar el ingreso al predio, se te entrega una pulsera magnetica RFID o llave numerada correspondiente a tu locker metalico reforzado para guardar bolsos y estuches rigidos.', 'Zona de Armado Tecnica', 'Ubicado justo al lado del sector de lockers, disponemos de bancos de trabajo tecnicos iluminados ideales para realizar la carga de baterias LiPo, recarga de gas y ajuste de Hop-Up.', 'img/almacenamiento_2.png', 'img/almacenamiento_3.png', 'Almacenamiento', 3);

INSERT IGNORE INTO CompetitivoEvent (id, title, description, image_url, badge, event_date, event_time, sort_order) VALUES
(1, 'Airsoft Premier Series', 'Inscribite en el torneo mensual por equipos. Modalidad 5vs5, mapa rotativo. Premios en efectivo y equipamiento para el equipo ganador.', 'img/ejercitos.jpg', 'Proximamente', '15 de Julio, 2026', '10:00 hs', 1),
(2, 'Campeonato Cruz del Sur', 'Torneo por equipos con fases clasificatorias y eliminacion directa. Partidas reglamentadas, mapas rotativos, diferentes modalidades de juego y premios para los primeros puestos.', 'img/soldado_argentino2.jpg', 'Nuevo', '22 de Julio, 2026', '14:00 hs', 2),
(3, 'Liga Condor', 'Competencia por fechas disputada a lo largo de la temporada. Los equipos acumulan puntos en cada jornada para definir la tabla general y los clasificados a la final.', 'img/ejercitos.jpg', 'Proximamente', '5 de Agosto, 2026', '09:00 hs', 3),
(4, 'Campeonato Condor Austral', 'Evento anual de formato competitivo con cupos limitados. Incluye arbitraje, cronograma de partidas y premios para los equipos destacados.', 'img/soldado_argentino2.jpg', 'Proximamente', '12 de Agosto, 2026', '20:00 hs', 4);
