from db import execute


def crear_mensaje(user_name, email, message):
    execute(
        "INSERT INTO ContactMessage (user_name, email, message) VALUES (%s, %s, %s)",
        (user_name, email, message),
    )
    return True


def listar_mensajes():
    return execute(
        "SELECT * FROM ContactMessage ORDER BY created_at DESC"
    )


def marcar_leido(message_id):
    execute("UPDATE ContactMessage SET leido = 1 WHERE id = %s", (message_id,))