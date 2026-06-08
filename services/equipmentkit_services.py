from db import execute
from dtos.errors import abort


def listar_kit_equipamientos(offset, limit):
    total_result = execute("SELECT COUNT(*) as total FROM EquipmentKit")
    total = total_result[0]['total']
    kits = execute(f"SELECT * FROM EquipmentKit LIMIT {limit} OFFSET {offset}")
    return kits, total


def obtener_kit_equipamiento(id):
    kits = execute(f"SELECT * FROM EquipmentKit WHERE id = {id}")
    if not kits:
        abort(404, 'Kit de equipamiento no encontrado')
    return kits[0]


def crear_kit_equipamiento(name, brand, price, quantity=1, purchase_link=None):
    brand_sql = f"'{brand}'" if brand is not None else "NULL"
    link_sql = f"'{purchase_link}'" if purchase_link else "NULL"
    execute(
        f"INSERT INTO EquipmentKit (name, brand, price, quantity, purchase_link) "
        f"VALUES ('{name}', {brand_sql}, {price}, {quantity}, {link_sql})"
    )


def reemplazar_kit_equipamiento(id, name, brand, price, quantity=1, purchase_link=None):
    kit = execute(f"SELECT id FROM EquipmentKit WHERE id = {id}")
    if not kit:
        abort(404, 'Kit de equipamiento no encontrado')
    brand_sql = f"'{brand}'" if brand is not None else "NULL"
    link_sql = f"'{purchase_link}'" if purchase_link else "NULL"
    execute(
        f"UPDATE EquipmentKit SET name = '{name}', brand = {brand_sql}, "
        f"price = {price}, quantity = {quantity}, purchase_link = {link_sql} "
        f"WHERE id = {id}"
    )


def eliminar_kit_equipamiento(id):
    kit = execute(f"SELECT id FROM EquipmentKit WHERE id = {id}")
    if not kit:
        abort(404, 'Kit de equipamiento no encontrado')
    execute(f"DELETE FROM EquipmentKit WHERE id = {id}")
    remaining = execute("SELECT COUNT(*) as total FROM EquipmentKit")
    if remaining[0]['total'] == 0:
        execute("ALTER TABLE EquipmentKit AUTO_INCREMENT = 1")
