from db import execute
from dtos.errors import abort


COLUMNS = "id, name, category, brand, description, image_url, price, quantity, purchase_link, details, sort_order"


def listar_kit_equipamientos(offset, limit, category='_all'):
    where = ""
    if category == '_all':
        pass
    elif category is None:
        where = "WHERE category IS NULL"
    else:
        where = f"WHERE category = '{category}'"
    total_result = execute(f"SELECT COUNT(*) as total FROM EquipmentKit {where}")
    total = total_result[0]['total']
    kits = execute(f"SELECT {COLUMNS} FROM EquipmentKit {where} ORDER BY sort_order ASC, id ASC LIMIT {limit} OFFSET {offset}")
    return kits, total


def obtener_kit_equipamiento(id):
    kits = execute(f"SELECT {COLUMNS} FROM EquipmentKit WHERE id = {id}")
    if not kits:
        abort(404, 'Kit de equipamiento no encontrado')
    return kits[0]


def crear_kit_equipamiento(name, brand, price, quantity=1, purchase_link=None,
                           category=None, description=None, image_url=None, details=None):
    brand_sql = f"'{brand}'" if brand is not None else "NULL"
    link_sql = f"'{purchase_link}'" if purchase_link else "NULL"
    cat_sql = f"'{category}'" if category else "NULL"
    desc_sql = f"'{description}'" if description else "NULL"
    img_sql = f"'{image_url}'" if image_url else "NULL"
    det_sql = f"'{details}'" if details else "NULL"
    execute(
        f"INSERT INTO EquipmentKit (name, category, brand, description, image_url, price, quantity, purchase_link, details) "
        f"VALUES ('{name}', {cat_sql}, {brand_sql}, {desc_sql}, {img_sql}, {price}, {quantity}, {link_sql}, {det_sql})"
    )


def reemplazar_kit_equipamiento(id, name, brand, price, quantity=1, purchase_link=None,
                                category=None, description=None, image_url=None, details=None):
    kit = execute(f"SELECT id FROM EquipmentKit WHERE id = {id}")
    if not kit:
        abort(404, 'Kit de equipamiento no encontrado')
    brand_sql = f"'{brand}'" if brand is not None else "NULL"
    link_sql = f"'{purchase_link}'" if purchase_link else "NULL"
    cat_sql = f"'{category}'" if category else "NULL"
    desc_sql = f"'{description}'" if description else "NULL"
    img_sql = f"'{image_url}'" if image_url else "NULL"
    det_sql = f"'{details}'" if details else "NULL"
    execute(
        f"UPDATE EquipmentKit SET name = '{name}', category = {cat_sql}, brand = {brand_sql}, "
        f"description = {desc_sql}, image_url = {img_sql}, "
        f"price = {price}, quantity = {quantity}, purchase_link = {link_sql}, details = {det_sql} "
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
