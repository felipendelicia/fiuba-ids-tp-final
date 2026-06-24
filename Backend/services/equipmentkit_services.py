from db import execute
from dtos.errors import abort


COLUMNS = "id, name, category, brand, description, image_url, price, quantity, purchase_link, details, sort_order"


def listar_kit_equipamientos(offset, limit, category='_all'):
    where = ""
    params = []
    if category == '_all':
        pass
    elif category is None:
        where = "WHERE category IS NULL"
    else:
        where = "WHERE category = %s"
        params.append(category)
    total_result = execute(f"SELECT COUNT(*) as total FROM EquipmentKit {where}", params)
    total = total_result[0]['total']
    query_params = params + [limit, offset]
    kits = execute(
        f"SELECT {COLUMNS} FROM EquipmentKit {where} ORDER BY sort_order ASC, id ASC LIMIT %s OFFSET %s",
        query_params
    )
    return kits, total


def obtener_kit_equipamiento(id):
    kits = execute(f"SELECT {COLUMNS} FROM EquipmentKit WHERE id = %s", (id,))
    if not kits:
        abort(404, 'Kit de equipamiento no encontrado')
    return kits[0]


def crear_kit_equipamiento(name, brand, price, quantity=1, purchase_link=None,
                           category=None, description=None, image_url=None, details=None):
    execute(
        "INSERT INTO EquipmentKit (name, category, brand, description, image_url, price, quantity, purchase_link, details) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (name, category, brand, description, image_url, price, quantity, purchase_link, details)
    )


def eliminar_kit_equipamiento(id):
    kit = execute("SELECT id FROM EquipmentKit WHERE id = %s", (id,))
    if not kit:
        abort(404, 'Kit de equipamiento no encontrado')
    execute("DELETE FROM EquipmentKit WHERE id = %s", (id,))
    remaining = execute("SELECT COUNT(*) as total FROM EquipmentKit")
    if remaining[0]['total'] == 0:
        execute("ALTER TABLE EquipmentKit AUTO_INCREMENT = 1")
