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

@app.route('/juegos',methods = ['GET']) #Sirve para mostrar todo el catalogo
def mostrar_catalogo():
    juegos = Juego.get_all()
    xml_response = '<?xml version="1.0" encoding="UTF-8"?><juegos>'
    for juego in juegos:
        xml_response += juego.to_xml()
    xml_response += '</juegos>'
    resp = flask.Response(xml_response, content_type='application/xml')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
    
@app.route('/juegos/filtros', methods = ['GET'])# Sirve para aplicar los filtros de la primera pagina
def juegos_filtros():
    xml_info = xmltodict.parse(request.data)
    #print(xml_info)
    query =''
    if xml_info["juego"]["titulo"] != None:
        query += f' WHERE titulo LIKE "%{xml_info["juego"]["titulo"]}%"'
    if xml_info["juego"]["desarrollador"] != None:
        if query != '':
            query += " AND"
        else:
            query += ' WHERE'
        query += f' desarrollador = "{xml_info["juego"]["desarrollador"]}"'
    if xml_info["juego"]["distribuidor"] != None:
        if query != '':
            query += " AND"
        else:
            query += " WHERE"
        query += f' distribuidor = "{xml_info["juego"]["distribuidor"]}"'
    
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

@app.route('/juegos/compra',methods = ['GET']) # Regresa la información de un juego 
def info_juego():
    xml_info = xmltodict.parse(request.data)
    if xml_info["juego"]["id"] != None:
        con = connect(DB_Admin.DB_NAME)
        cur = con.cursor()
        cur.execute(f'SELECT * FROM juegos WHERE id = "{xml_info["juego"]["id"]}"')
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
    else:
        resp = make_response(dumps({'response' : 'Error'},404))
        resp.headers.extend(headers or {})
        return resp
        
@app.route('/juego/compras/transaccion',methods = ['PUT'])
def transaccion():
    id = 4
    idjuego = 1
    con = connect(DB_Admin.DB_NAME)
    cur = con.cursor()
    cur.execute(f'SELECT credito FROM usuarios WHERE id = {id}')
    creditoUsuario = cur.fetchall()
    cur.execute(f'SELECT precio FROM juego WHERE id = {idjuego}')
    precioJuego = cur.fetchall()
    nuevoCredito = creditoUsuario - precioJuego
    if nuevoCredito >= 0:
        cur.execute(f'UPDATE usuarios SET credito = {nuevoCredito} WHERE id = {id}')
        con.close()
        resp = make_response(dumps({},200))
        return resp
    else:
        con.close()
        resp = make_response(dumps({"mensaje" : "No tienes credito suficiente"},404))
        return resp
    

if __name__ == '__main__':
    DB_Admin.start_db()
    app.run(debug=True, port=4000)
