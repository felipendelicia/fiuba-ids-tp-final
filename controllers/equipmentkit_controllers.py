from db import obtener_conexion

def db_seleccionar_todos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT id, name, type, price, stock FROM equipments")
    lista = cursor.fetchall()
    cursor.close()
    conexion.close()
    return lista

def db_seleccionar_por_id(id_equipment):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT id, name, type, price, stock FROM equipments WHERE id = %s", (id_equipment,))
    equipamiento = cursor.fetchone()
    cursor.close()
    conexion.close()
    return equipamiento

def db_insertar_equipamiento(name, tipo, price, stock):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO equipments (name, type, price, stock) VALUES (%s, %s, %s, %s)",
                   (name, tipo, price, stock))
    conexion.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    conexion.close()
    return nuevo_id

def db_actualizar_equipamiento(id_equipment, name, tipo, price, stock):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("UPDATE equipments SET name = %s, type = %s, price = %s, stock = %s WHERE id = %s",
                   (name, tipo, price, stock, id_equipment))
    conexion.commit()
    filas = cursor.rowcount
    cursor.close()
    conexion.close()
    return filas

def db_eliminar_equipamiento(id_equipment):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM equipments WHERE id = %s", (id_equipment,))
    conexion.commit()
    filas = cursor.rowcount
    cursor.close()
    conexion.close()
    return filas
