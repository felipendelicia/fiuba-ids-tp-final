from db import execute


def listar_kit_equipamientos(id, name, brand, price):
    x = f"NSERT INTO EquipmentKit(id, name, brand, price) VALUE({id}, '{name}', '{brand}', {price}"
