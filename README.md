# Introducción al desarrollo de software (FIUBA)

## Integrantes:
- Felipe Nahuel Delicia 115775 
- Dante Ghisi 115735
- Balderrama Rubin de Celis Mariano 115667
- Suarez Hans Leonardo 115120
- Gabriel Alexander Saavedra 114419
- Ronny Mamani Torrez 114779
- Kiliano Agustin Olivera 115740

## Descripción:

Este proyecto consta en una plataforma web integral dedicada a 
la reserva de turnos y gestión de predios para el deporte airsoft.

## Funcionalidades:

- Visualizar y seleccionar horarios disponibles, tipos de escenarios/canchas y servicios adicionales
- Registro y autenticación segura de usuarios
- Perfil del jugador
- Realizar reseñas de canchas


## Levantar con Docker:

```bash
docker compose up --build
```

```obs: en .env.example, se pueden descomentar los valores del email para poder utilizar el de kinetix o usar otro email empresarial```

## Servicios

| Servicio | Puerto | URL |
|----------|--------|-----|
| Frontend | 5000 | http://localhost:5000 |
| Backend  | 8000 | http://localhost:8000 |
| MySQL    | 3307 | localhost:3307 |

## Comandos útiles

```bash
# Detener contenedores
docker compose down

# Ver logs
docker compose logs -f

# Reconstruir sin cache
docker compose up --build
```

## Estructura del proyecto

```
Backend/
├── app.py               # Entry point
├── controllers/         # Request handlers
├── routes/              # Route registrations
├── services/            # Business logic
├── dtos/                # Validation & responses
├── db.py                # Database connection
└── schema.sql           # DB schema

Frontend/
├── app.py               # Entry point (8 líneas)
├── helpers.py           # API helpers (_api_get, _api_post, etc.)
├── routes/              # Route modules agrupados por dominio
│   ├── public.py        # index, campos, modalidades, servicios
│   ├── auth.py          # login, registro, contraseña
│   ├── profile.py       # perfil, favoritos, reseñas
│   ├── reservations.py  # reservas, lobbies, turnos
│   └── admin.py         # dashboard, usuarios, equipamiento, modalidades
├── services/            # Dashboard services
├── templates/           # Jinja2 templates
└── static/              # CSS, JS, images
```
