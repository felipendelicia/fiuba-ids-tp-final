from db import execute


def listar_categorias():
    rows = execute("SELECT * FROM EquipmentCategory ORDER BY sort_order ASC")
    return rows