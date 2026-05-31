# Airsoft Project
# Introducción al desarrollo de software (FIUBA)

## Integrantes:
- Felipe Nahuel Delicia 115775
- Dante Ghisi 115735
- Balderrama Rubin de Celis Mariano 115667
- Suarez Hans Leonardo 115120
- Franchini Juan Luca 115800
- Gabriel Alexander Saavedra 114419
- Ronny Mamani Torrez 114779
- Kiliano Agustin Olivera 115740
- Gabriel Vera 114517

## Descripción:

Este proyecto consta en una plataforma web integral dedicada a 
la reserva de turnos y gestión de predios para el deporte airsoft.

## Funcionalidades:

- Visualizar y seleccionar horarios disponibles, tipos de escenarios/canchas y servicios adicionales
- Registro y autenticación segura de usuarios
- Perfil del jugador
- Realizar reseñas de canchas

## Instalación:

En el directorio del proyecto:

### Configurar variables de entorno
```cp .env.example .env```

Editar el archivo .env con las credenciales de la base de datos

### Crear un entorno virtual e instalar las dependencias

```
python3 -m venv .venv  
source .venv/bin/activate
pip install -r requirements.txt
```

### Crear esquema de base de datos

```Observación: El schema.sql está configurado para crear una base de datos por defecto llamada "airsoftdb"```

```sudo mysql -u root -p < schema.sql```

### Ejecutar el servidor

```python3 app.py```







- 
- 
-
-
-
