# Importamos la función:
from db import execute


def db_seleccionar_todos():
    query = "SELECT id, name, type, price, stock FROM equipments"
    return execute(query)


def db_seleccionar_por_id(id_equipment):
    query = f"SELECT id, name, type, price, stock FROM equipments WHERE id = {id_equipment}"
    resultados = execute(query)
    # Si la lista tiene elementos, devolvemos el primero (el equipamiento encontrado)
    if resultados:
        return resultados[0]
    return None


def db_insertar_equipamiento(name, tipo, price, stock):
    # Armamos la consulta para insertar los datos en MySQL
    query = f"INSERT INTO equipments (name, type, price, stock) VALUES ('{name}', '{tipo}', {price}, {stock})"
    execute(query)

    # Para saber qué ID se creó, buscamos el último insertado
    query_id = "SELECT LAST_INSERT_ID() as id"
    resultado_id = execute(query_id)
    return resultado_id[0]['id']


def db_actualizar_equipamiento(id_equipment, name, tipo, price, stock):
    query = f"UPDATE equipments SET name = '{name}', type = '{tipo}', price = {price}, stock = {stock} WHERE id = {id_equipment}"
    resultado = execute(query)
    if resultado is False:
        return 0
    return 1  # Retornamos 1 para simular que se afectó la fila correctamente


def db_eliminar_equipamiento(id_equipment):
    query = f"DELETE FROM equipments WHERE id = {id_equipment}"
    resultado = execute(query)
    if resultado is False:
        return 0
    return 1
