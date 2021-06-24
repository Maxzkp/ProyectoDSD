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

@app.route('/juegos/visualizarCompra',methods = ['GET']) # Regresa la información de un juego 
def info_juego():
    xml_info = xmltodict.parse(request.data)
    if xml_info["juegos"]["juego"]["id"] != None:
        con = connect(DB_Admin.DB_NAME)
        cur = con.cursor()
        cur.execute(f'SELECT * FROM juegos WHERE id = "{xml_info["juegos"]["juego"]["id"]}"')
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
        xml_response = '<?xml version="1.0" encoding="UTF-8"?><errorJuegos>'
        xml_response = f'<error>No se envio id de juego</error>'
        xml_response += '</errorJuegos>'
        resp = flask.Response(xml_response, content_type='application/xml')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
        
@app.route('/juego/compras/actualizarCredito',methods = ['PUT']) #resta el precio al credito
def actualizar_credito():
    xml_info = xmltodict.parse(request.data)
    if xml_info["compra"]["usuario"]["id"] != None:
        if ["compra"]["juego"]["id"] != None:
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
                xml_response = '<?xml version="1.0" encoding="UTF-8"?><errorCredito>'
                xml_response = f'<error>El usuario no tiene el suficiente credito</error>'
                xml_response += '</errorCredito>'
                resp = flask.Response(xml_response, content_type='application/xml')
                resp.headers['Access-Control-Allow-Origin'] = '*'
                return resp
        else:
            con.close()
            xml_response = '<?xml version="1.0" encoding="UTF-8"?><errorCredito>'
            xml_response = f'<error>No se encuentra el juego deseado</error>'
            xml_response += '</errorCredito>'
            resp = flask.Response(xml_response, content_type='application/xml')
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        else:
        con.close()
        xml_response = '<?xml version="1.0" encoding="UTF-8"?><errorCredito>'
        xml_response = f'<error>No se encuentra el usuario</error>'
        xml_response += '</errorCredito>'
        resp = flask.Response(xml_response, content_type='application/xml')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

@app.route('/juegos/registros', methods = ['POST'])
def nuevo_juego():
    xml_info = xmltodict.parse(request.data)
    if xml["juegos"]["juego"]["id"] != None:
        juego = Juego((None, xml["juegos"]["juego"]["id"], xml["juegos"]["juego"]["desarrollador"], xml["juegos"]["juego"]["distribuidor"], xml["juegos"]["juego"]["fechalanzamiento"], xml["juegos"]["juego"]["descripcion"], xml["juegos"]["juego"]["precio"]))
        juego.save()
        juegos = Juego.get_all()
        return str([str(juego) for juego in juegos])
    


if __name__ == '__main__':
    DB_Admin.start_db()
    app.run(debug=True, port=4000)