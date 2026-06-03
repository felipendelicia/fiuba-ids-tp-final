from db import execute
from dtos.errors import abort


def listar_kit_equipamientos(offset, limit):
    total_result = execute("SELECT COUNT(*) as total FROM EquipmentKit")
    total = total_result[0]['total']
    kits = execute(f"SELECT * FROM EquipmentKit LIMIT {limit} OFFSET {offset}")
    return kits, total


def crear_kit_equipamiento(name, brand, price):
    brand_sql = f"'{brand}'" if brand is not None else "NULL"
    execute(
        f"INSERT INTO EquipmentKit (name, brand, price) "
        f"VALUES ('{name}', {brand_sql}, {price})"
    )


def reemplazar_kit_equipamiento(id, name, brand, price):
    kit = execute(f"SELECT id FROM EquipmentKit WHERE id = {id}")
    if not kit:
        abort(404, 'Kit de equipamiento no encontrado')
    brand_sql = f"'{brand}'" if brand is not None else "NULL"
    execute(
        f"UPDATE EquipmentKit SET name = '{name}', brand = {brand_sql}, price = {price} WHERE id = {id}"
    )


def eliminar_kit_equipamiento(id):
    kit = execute(f"SELECT id FROM EquipmentKit WHERE id = {id}")
    if not kit:
        abort(404, 'Kit de equipamiento no encontrado')
    execute(f"DELETE FROM EquipmentKit WHERE id = {id}")
