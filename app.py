from flask import Flask, request
import xmltodict
from ORM.models import DB_Admin, Juego

app = Flask(__name__)

@app.route('/')
def main():
    #Juego.clear_all()
    juego = Juego((None, 'Juego 1', 'dev', 'dis', 'DD MMM AAAA', 'qdboauysdbuwdq', 1000))
    juego.save()
    juegos = Juego.get_all()
    return str([str(juego) for juego in juegos])

@app.route('/juegos', methods = ['POST'])
def juegos():
    xml_info = xmltodict.parse(request.data)
    try:
        action = xml_info['juego']['@action']
    except:
        action = None

    if action == 'getall':
        juegos = Juego.get_all()
        xml_response = '<?xml version="1.0" encoding="UTF-8"?><juegos>'
        for juego in juegos:
            xml_response += juego.to_xml()
        xml_response += '</juegos>'
        return xml_response
    if action == 'getby':
        juegos = Juego.get_by(xml_info['juego']['id'], xml_info['juego']['titulo'])
        xml_response = '<?xml version="1.0" encoding="UTF-8"?><juegos>'
        for juego in juegos:
            xml_response += juego.to_xml()
        xml_response += '</juegos>'
        return xml_response
    else:
        return xml_info
    
if __name__ == '__main__':
    DB_Admin.start_db()
    app.run(debug=True)