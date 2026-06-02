from flask import request
import os
from dotenv import load_dotenv
from db import execute

from email.message import EmailMessage
import ssl
import smtplib

import qrcode
import io

load_dotenv()



def build_links(total, offset, limit):
    """Construye los links HATEOAS para navegar entre páginas"""
    base_url = request.base_url

    # Mantener filtros actuales (equipo, fecha, fase, etc.) en los links
    extra = ""
    for key, value in request.args.items():
        if key not in ('_offset', '_limit'):
            extra += f"&{key}={value}"

    def make_url(off):
        return f"{base_url}?_offset={off}&_limit={limit}{extra}"

    last_offset = max(0, ((total - 1) // limit) * limit) if total > 0 else 0
    prev_offset = max(0, offset - limit)
    next_offset = min(last_offset, offset + limit)

    return {
        "_first": {"href": make_url(0)},
        "_prev": {"href": make_url(prev_offset)},
        "_next": {"href": make_url(next_offset)},
        "_last": {"href": make_url(last_offset)}
    }


def send_reservation_mail(email_reciver, body):
    try:
        email_sender= os.getenv("EMAIL")
        password= os.getenv("EMAIL_PASSWORD")

        subject = f"Reserva de airsoft: {body.get('reservation_date')}"
        
        map_result= execute(f"SELECT name FROM Maps WHERE id = {body.get('map_id')}")
        map_name= map_result[0]['name'] if map_result else "Desconocido (consultar con personal)" #Acá sino se puede optar por no mandar el mail si no encuentra el mapa
        
        
        email_body = f"""¡Tu reserva de Airsoft está confirmada!
        **ID Usuario: {body.get('account_id')} **
        **Mapa seleccionado: {map_name} **
        **Horario: {body.get('start_time')} a {body.get('end_time')} **
        Gracias por reservar!"""

        QR_code= qr_generator(body)
        
        em= EmailMessage()
        em["From"]= email_sender
        em["To"]= email_reciver
        em["Subject"]= subject
        em.set_content(email_body)
        em.add_attachment(QR_code, maintype='image', subtype='png', filename='qr.png')
        
        context= ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com",465,context = context) as smtp:
            smtp.login(email_sender, password)
            smtp.sendmail(email_sender, email_reciver, em.as_string())

        return True
    
    except:
        return False


def qr_generator(body):
    public = "Si" if body.get('is_public') else "No"
    qr_input= f"ID Usuario: {body.get('account_id')}, Reserva: {body.get('reservation_date')}, Pública: {public}"

    qr = qrcode.QRCode(version= 1, box_size= 10, border= 5)
    qr.add_data(qr_input)
    qr.make(fit=True)

    QR_img= qr.make_image(fill='black', back_color='white')
    #QR en memoria de bytes para no guardar QRS
    img_byte_arr= io.BytesIO()
    QR_img.save(img_byte_arr, format='PNG')

    return img_byte_arr.getvalue()



