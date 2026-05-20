rom flask import Flask, render_template

app = Flask(__name__)

# pantalla de Servicios
@app.route('/servicios')
def servicios():
    # lo que devolvería tu base de datos MySQL
    modos_prueba = [
        {"id": 1, "name": "Captura la Bandera", "description": "Llevá la bandera enemiga a tu base.", "duration": 45, "number_players": 20, "price": 4500.50},
        {"id": 2, "name": "Team Deathmatch", "description": "Eliminá al equipo contrario.", "duration": 30, "number_players": 16, "price": 3000.00}
    ]
    return render_template('services.html', gamemodes=modos_prueba)

# pantalla de Contacto
@app.route('/contacto')
def contacto():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)



