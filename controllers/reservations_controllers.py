from flask import request, jsonify
from db import execute
from errors import ERRORS
from helpers import build_links
from helpers import send_reservation_mail
from services.reservations_services import ( 
    listar_reservas as listar_service,
    listar_reservas_usuario as listar_reservas_usuario_service,
    crear_reserva as crear_service,
    actualizar_reserva as actualizar_service
    #crear_public_reservation as crear_public_service
)



def listar_reservas():
    start_time= request.args.get('start_time')
    end_time= request.args.get('end_time')
    #created_at= request.args.get('created_at') # Este no aplica como filtro en principio
    is_public= request.args.get('is_public')


    try:
        limit= int(request.args.get('_limit', 10))
        offset= int(request.args.get('_offset', 0))

    except ValueError:
        return ERRORS["INVALID_FORMAT"]("Los parámetros de paginación deben ser números enteros")

    if limit < 1 or offset < 0:
        return ERRORS["INVALID_FORMAT"]("Parámetros de paginación inválidos")

    reservas, total= listar_service(offset, limit, start_time, end_time, is_public)

    if reservas is None:
        return ERRORS['UNKNOWN_ERROR']('Error al obtener reservas')

    links= build_links(total, offset, limit)

    return jsonify({'reservas': reservas, 'total': total, 'links': links}), 200

 


def listar_reservas_usuario(id):

    try:
        limit= int(request.args.get('_limit', 10))
        offset= int(request.args.get('_offset', 0))

    except ValueError:
        return ERRORS["INVALID_FORMAT"]("Los parámetros de paginación deben ser números enteros")

    if limit < 1 or offset < 0:
        return ERRORS["INVALID_FORMAT"]("Parámetros de paginación inválidos")

    reservas, total= listar_reservas_usuario_service(offset, limit, id)

    if reservas is None:
        return ERRORS['UNKNOWN_ERROR']('Error al obtener reservas')

    links= build_links(total, offset, limit)

    return jsonify({'reservas': reservas, 'total': total, 'links': links}), 200


 

def crear_reserva(id):
    body= request.get_json()

    if not body:
        return ERRORS["MISSING_REQUIRED_FIELDS"]("No mandaste el body")
    

    account_id= body.get('account_id')
    #game_mode_id= body.get('game_mode_id') #Uso el id del parámetro crear_reserva para el game mode
    map_id= body.get('map_id')
    equipment_kit_id= body.get('equipment_kit_id')
    price= body.get('price')
    is_public = False   #is_public= body.get('is_public')
    reservation_date= body.get('reservation_date')
    start_time= body.get('start_time')
    end_time= body.get('end_time')


    
    #game_mode_result= execute(f"SELECT * FROM GameModes WHERE game_mode_id = {id}")
    game_mode_result= execute(f"SELECT * FROM GameModes WHERE id = {id}")
    if not game_mode_result:
        return ERRORS["NOT_FOUND"]("No se encontró el modo de juego")

    max_players= game_mode_result[0]['players']

    # VERIFICO QUE HAYA LUGAR PARA QUE EL USUARIO SE PUEDA REGISTRAR EN LA PARTIDA
    success, error= crear_service(account_id, id, map_id, equipment_kit_id, price, is_public,
                                    reservation_date, start_time, end_time, max_players)

    if error == 'conflict':
        return ERRORS['CONFLICT']('No se puede registar en la partida')

    # ACÁ LE MANDO AL EMAIL USADO EL QR:
    user_result = execute(f"SELECT email FROM Accounts WHERE id = {account_id}")
    if not user_result:
        return ERRORS["NOT_FOUND"]("No se encontró el usuario con ese id")

    user_email= user_result[0]['email']

    send_email= send_reservation_mail(user_email, body)

    if not send_email:
        print("Advertencia: La reserva se creó pero el mail no pudo enviarse")
    

    return jsonify({"message": "Reserva creada exitosamente"}), 200




def actualizar_reserva(id):
    data= request.get_json()

    if not data:
        return ERRORS["MISSING_REQUIRED_FIELDS"]("No mandaste el body")

    updated_reservation= actualizar_service(id, data)

    if updated_reservation is None:
        return ERRORS['UNKNOWN_ERROR']('Error al actualizar la reserva')

    if updated_reservation is False:
        return ERRORS['NOT_FOUND'](f"Reserva con ID {id} no encontrada")

    return jsonify({"message": "Reserva {id} actualizada correctamente"}), 200
        


    

    

# Se encuentra en otra ruta que la de crear_reserva, en caso que se quiera cambiar, se puede integrar todo en crear_reserva
def crear_public_reservation(id):
    body= request.get_json()

    if not body:
        return ERRORS["MISSING_REQUIRED_FIELDS"]("No mandaste el body")
    

    account_id= body.get('account_id')
    map_id= body.get('map_id')
    equipment_kit_id= body.get('equipment_kit_id')
    price= body.get('price')
    is_public = True
    reservation_date= body.get('reservation_date')
    start_time= body.get('start_time')
    end_time= body.get('end_time')

    
    game_mode_result= execute(f"SELECT * FROM GameModes WHERE id = {id}")
    if not game_mode_result:
        return ERRORS["NOT_FOUND"]("No se encontró el modo de juego")

    max_players= game_mode_result[0]['players']

    # VERIFICO QUE HAYA LUGAR PARA QUE EL USUARIO SE PUEDA REGISTRAR EN LA PARTIDA
    success, error= crear_service(account_id, id, map_id, equipment_kit_id, price, is_public,
                                    reservation_date, start_time, end_time, max_players)

    if error == 'conflict':
        return ERRORS['CONFLICT']('No se puede registar en la partida')

    # ACÁ LE MANDO AL EMAIL USADO EL QR:
    user_result = execute(f"SELECT email FROM Accounts WHERE id = {account_id}")
    
    if not user_result:
        return ERRORS["NOT_FOUND"]("No se encontró el usuario con ese id")

    user_email= user_result[0]['email']

    send_email= send_reservation_mail(user_email, body)

    if not send_email:
        print("Advertencia: La reserva se realizó pero el mail no pudo enviarse")
    

    return jsonify({"message": "Reserva creada exitosamente"}), 200
 



    
