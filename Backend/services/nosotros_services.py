from db import execute


def obtener_info():
    rows = execute("SELECT * FROM NosotrosInfo WHERE section = 'main'")
    return rows[0] if rows else None


def listar_cards():
    return execute("SELECT * FROM NosotrosCard ORDER BY sort_order ASC")