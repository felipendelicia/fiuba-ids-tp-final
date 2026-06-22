from flask import render_template, request, redirect, url_for, session
from helpers import _api_get_maps, _api_get_gamemodes, _api_get_equipmentkits, _api_get_equipment_categories, _api_get_competitivo_events, _api_get_nosotros, _api_get_services, _api_get_service


def register(app):

    @app.route("/")
    def index():
        return render_template('index.html', usuario=session.get('usuario'))

    @app.route("/campos")
    def campos():
        mapas = _api_get_maps()
        return render_template('campos.html', usuario=session.get('usuario'), mapas=mapas)

    @app.route('/campos/informacion/planonuketown')
    def info_mapa_index():
        return render_template('nuketown_plano.html', usuario=session.get('usuario'))

    @app.route('/campos/informacion/planomirage')
    def info_mapa_index2():
        return render_template('mirage_plano.html', usuario=session.get('usuario'))

    @app.route('/campos/informacion/planohijacked')
    def info_mapa_index3():
        return render_template('hijacked_plano.html', usuario=session.get('usuario'))

    @app.route('/campos/informacion/planoterminal')
    def info_mapa_index4():
        return render_template('terminal_plano.html', usuario=session.get('usuario'))

    @app.route('/campos/informacion/<nombre_mapa>')
    def info_mapa(nombre_mapa):
        mapas = _api_get_maps()
        for mapa in mapas:
            if mapa["name"].lower() == nombre_mapa:
                return render_template(f'info_mapa.html', mapa=mapa, usuario=session.get('usuario'))
        return render_template('404.html'), 404

    @app.route('/campos/informacion/<nombre_mapa>/plano')
    def info_mapa_plano(nombre_mapa):
        mapas = _api_get_maps()
        for mapa in mapas:
            if mapa["name"].lower() == nombre_mapa:
                return render_template(f'plano_mapa.html', mapa=mapa, usuario=session.get('usuario'))
        return render_template('404.html'), 404

    @app.route('/servicios')
    def servicios():
        servicios = _api_get_services()
        return render_template('servicios.html', servicios=servicios, usuario=session.get('usuario'))

    @app.route('/servicios/buffet')
    def servicio_buffet():
        s = _api_get_service(1)
        return render_template('servicio_detalle.html', s=s, usuario=session.get('usuario'))

    @app.route('/servicios/estacionamiento')
    def servicio_estacionamiento():
        s = _api_get_service(2)
        return render_template('servicio_detalle.html', s=s, usuario=session.get('usuario'))

    @app.route('/servicios/almacenamiento')
    def servicio_almacenamiento():
        s = _api_get_service(3)
        return render_template('servicio_detalle.html', s=s, usuario=session.get('usuario'))

    @app.route("/nosotros")
    def nosotros():
        data = _api_get_nosotros()
        return render_template('nosotros.html', info=data.get('info', {}), cards=data.get('cards', []), usuario=session.get('usuario'))

    @app.route("/competitivo")
    def competitivo():
        events = _api_get_competitivo_events()
        return render_template("competitivo.html", events=events, usuario=session.get('usuario'))

    @app.route('/equipamiento')
    def equipamiento():
        categorias = _api_get_equipment_categories()
        return render_template('equipamiento.html', categorias=categorias, usuario=session.get('usuario'))

    @app.route('/equipamientoinfo/armasinfo')
    def equipamiento_armas():
        items = _api_get_equipmentkits(category='arma')
        cats = _api_get_equipment_categories()
        cat_info = next((c for c in cats if c['slug'] == 'arma'), {})
        return render_template('equipamiento_armas.html', items=items, cat_info=cat_info, usuario=session.get('usuario'))

    @app.route('/equipamientoinfo/chaleco')
    def equipamiento_chaleco():
        items = _api_get_equipmentkits(category='chaleco')
        cats = _api_get_equipment_categories()
        cat_info = next((c for c in cats if c['slug'] == 'chaleco'), {})
        return render_template('equipamiento_chaleco.html', items=items, cat_info=cat_info, usuario=session.get('usuario'))

    @app.route('/equipamientoinfo/casco')
    def equipamiento_casco():
        items = _api_get_equipmentkits(category='casco')
        cats = _api_get_equipment_categories()
        cat_info = next((c for c in cats if c['slug'] == 'casco'), {})
        return render_template('equipamiento_casco.html', items=items, cat_info=cat_info, usuario=session.get('usuario'))

    @app.route("/modalidades")
    def modalidades():
        events = _api_get_competitivo_events()
        return render_template('modalidades.html', modalidades=_api_get_gamemodes(), events=events, usuario=session.get('usuario'))

    @app.route("/resenias")
    def opciones_resenias():
        usuario = session.get('usuario')
        return render_template('resenias_opciones.html', usuario=usuario)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404
