from flask import Flask, request
import flask
import xmltodict
from ORM.models import DB_Admin, Juego
from flask_cors import CORS
from sqlite3 import connect

app = Flask(__name__)
CORS(app)

@app.route('/')
def main():
    #Juego.clear_all()
    juego = Juego((None, 'Juego 1', 'dev', 'dis', 'DD MMM AAAA', 'qdboauysdbuwdq', 1000))
    juego.save()
    juegos = Juego.get_all()
    return str([str(juego) for juego in juegos])

@app.route('/juegos',methods = ['GET'])
def mostrar_catalogo():
    juegos = Juego.get_all()
    xml_response = '<?xml version="1.0" encoding="UTF-8"?><juegos>'
    for juego in juegos:
        xml_response += juego.to_xml()
    xml_response += '</juegos>'
    resp = flask.Response(xml_response, content_type='application/xml')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
    
@app.route('/juegos/filtros', methods = ['GET'])
def juegos_filtros():
    xml_info = xmltodict.parse(request.data)
    #print(xml_info)
    query =''
    if xml_info["juegos"]["juego"]["titulo"] != None:
        query += f' WHERE titulo LIKE "%{xml_info["juegos"]["juego"]["titulo"]}%"'
    if xml_info["juegos"]["juego"]["desarrollador"] != None:
        if query != '':
            query += " AND"
        else:
            query += ' WHERE'
        query += f' desarrollador = "{xml_info["juegos"]["juego"]["desarrollador"]}"'
    if xml_info["juegos"]["juego"]["distribuidor"] != None:
        if query != '':
            query += " AND"
        else:
            query += " WHERE"
        query += f' distribuidor = "{xml_info["juegos"]["juego"]["distribuidor"]}"'
    
    con = connect(DB_Admin.DB_NAME)
    cur = con.cursor()
    cur.execute(f'SELECT * FROM juegos{query}')
    dats = cur.fetchall()
    juegos = [Juego(dat) for dat in dats]
    con.close()
    #print(dats)
    xml_response = '<?xml version="1.0" encoding="UTF-8"?><juegosFiltros>'
    for juego in juegos:
        xml_response += juego.to_xml()
    xml_response += '</juegosFiltros>'
    resp = flask.Response(xml_response, content_type='application/xml')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == '__main__':
    DB_Admin.start_db()
    app.run(debug=True, port=4000)