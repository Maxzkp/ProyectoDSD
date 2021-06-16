from sqlite3 import connect

class DB_Admin():

    DB_NAME = 'SS.sqlite3'

    @classmethod
    def start_db(self):
        con = connect(self.DB_NAME)

        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS juegos("+
        "id INTEGER PRIMARY KEY,"+
        "titulo VARCHAR(255),"+
        "desarrollador VARCHAR(255),"+
        "distribuidor VARCHAR(255),"+
        "lanzamiento VARCHAR(255),"+
        "descripcion TEXT,"+
        "precio INT(10)"+
        ")")

        cur.execute("CREATE TABLE IF NOT EXISTS usuarios("+
        "id INTEGER PRIMARY KEY,"+
        "username VARCHAR(255),"+
        "email VARCHAR(255),"+
        "password VARCHAR(255),"+
        "credito INT(10)"+
        ")")

        cur.execute("CREATE TABLE IF NOT EXISTS compras("+
        "id INTEGER PRIMARY KEY,"+
        "fecha VARCHAR(255),"+
        "hora VARCHAR(255),"+
        "ususario INT(10),"+
        "juego INT(10)"+
        ")")

        con.close()        

class Juego:

    def __init__(self, dats=(0, 'title', 'dev', 'dis', 'lanz', 'desc', 0)) -> None:
        self.id = dats[0]
        self.title = dats[1]
        self.desarrollador = dats[2]
        self.distribuidor = dats[3]
        self.fechalanzamiento = dats[4]
        self.descripcion = dats[5]
        self.precio = dats[6]

    def __str__(self) -> str:  
        return f'{self.id}: {self.title} {self.precio}'

    def to_xml(self):
        id = f'<id>{self.id}</id>'
        title = f'<titulo>{self.title}</titulo>'
        desarrollador = f'<desarrollador>{self.desarrollador}</desarrollador>'
        distribuidor = f'<distribuidor>{self.distribuidor}</distribuidor>'
        fechalanzamiento = f'<fechalanzamiento>{self.fechalanzamiento}</fechalanzamiento>'
        descripcion = f'<descripcion>{self.descripcion}</descripcion>'
        precio = f'<precio min="" max="">{self.precio}</precio>'
        return f'<juego action="success">{id}{title}{desarrollador}{distribuidor}{fechalanzamiento}{descripcion}{precio}</juego>'

    @classmethod
    def get_all(self):
        con = connect(DB_Admin.DB_NAME)
        cur = con.cursor()
        cur.execute('SELECT * FROM juegos')
        dats = cur.fetchall()
        juegos = [Juego(dat) for dat in dats]
        con.close()
        return juegos
    
    @classmethod
    def get_by(self, id = None, title=None):
        query = ''
        if id != None:
            query += f' WHERE id = {id}'
        if title != None:
            if query != '':
                query += ' AND'
            else:
                query += ' WHERE'
            query += f' titulo LIKE "%{title}%"'

        con = connect(DB_Admin.DB_NAME)
        cur = con.cursor()
        cur.execute(f'SELECT * FROM juegos{query}')
        dats = cur.fetchall()
        juegos = [Juego(dat) for dat in dats]
        con.close()
        return juegos

    def save(self):
        con = connect(DB_Admin.DB_NAME)
        cur = con.cursor()
        cur = con.execute(f'INSERT INTO juegos VALUES (null, "{self.title}", "{self.desarrollador}", "{self.distribuidor}", "{self.fechalanzamiento}", "{self.descripcion}", {self.precio})')
        con.commit()
        con.close()

    #Debug
    @classmethod
    def clear_all(self):
        con = connect(DB_Admin.DB_NAME)
        cur = con.cursor()
        cur.execute('DELETE FROM juegos')
        con.commit()
        con.close()