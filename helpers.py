from flask import request



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
    # API de RESEND "pública"
    API_KEY= "re_NKV5ciJX_6BFuMQ7VAHHJmiadxY3vVjKR"                

    subject = f"Reserva de airsoft: {body.get('reservation_date')}"
    
    
    email_html = f"""
    <h3>¡Tu reserva de Airsoft está confirmada!</h3>
    <p><b>ID Usuario:</b> {body.get('account_id')}</p>
    <p><b>Mapa seleccionado:</b> {body.get('map_id')}</p>
    <p><b>Horario:</b> {body.get('start_time')} a {body.get('end_time')}</p>
    <br>
    <p><i>Gracias por reservar!</i></p>
    """

    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "from": "Airsoft Sistema <onboarding@resend.dev>",
        "to": email_reciver,
        "subject": subject,
        "html": email_html
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200 or response.status_code == 201:
            return True
        
        else:
            print(f"\n ERROR DE RESEND (Status {response.status_code}):")
            print(f"Respuesta de la API: {response.text}\n")
            return False

    
    except Exception as e:
        return False
