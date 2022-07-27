from flask import Flask ,jsonify,request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app=Flask(__name__)
CORS(app)
# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://marbara:11Mar1967=@db4free.net/marcelo1967'
# app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost/flaskmysql'
#                                                 user:clave@localhost/nombreBaseDatos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db= SQLAlchemy(app)
ma=Marshmallow(app)
# defino la tabla
class Equipo(db.Model):   # la clase Equipo hereda de db.Model     
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    imagen=db.Column(db.String(150))
    nombre=db.Column(db.String(100))
    cantesc=db.Column(db.Integer)
    canttot=db.Column(db.Integer)
    def __init__(self,imagen,nombre,cantesc,canttot):   #crea el  constructor de la clase
        self.imagen=imagen
        self.nombre=nombre   # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.cantesc=cantesc
        self.canttot=canttot
db.create_all()  # crea las tablas
#  ************************************************************
class EquipoSchema(ma.Schema):
    class Meta:
        fields=('id','imagen','nombre','cantesc','canttot')
equipo_schema=EquipoSchema()            # para crear un equipo
equipos_schema=EquipoSchema(many=True)  # multiples registros
@app.route('/')
def index():
    return "<h1>Corriendo Servidor Flask</h1>"
@app.route('/equipos',methods=['GET'])
def get_Equipos():
    all_equipos=Equipo.query.all()     # query.all() lo hereda de db.Model
    result=equipos_schema.dump(all_equipos)  # .dump() lo hereda de ma.schema
    return jsonify(result)
@app.route('/equipos/<id>',methods=['GET'])
def get_equipo(id):
    equipo=Equipo.query.get(id)
    return equipo_schema.jsonify(equipo)
@app.route('/equipo/<id>',methods=['DELETE'])
def delete_equipo(id):
    equipo=Equipo.query.get(id)
    db.session.delete(equipo)
    db.session.commit()
    return equipo_schema.jsonify(equipo)
@app.route('/equipos', methods=['POST']) # crea ruta o endpoint
def create_equipo():
    print(request.json)  # request.json contiene el json que envio el cliente
    imagen=request.json['imagen']
    nombre=request.json['nombre']
    cantesc=request.json['cantesc']
    canttot=request.json['canttot']
    new_equipo=Equipo(imagen,nombre,cantesc,canttot)
    db.session.add(new_equipo)
    db.session.commit()
    return equipo_schema.jsonify(new_equipo)
@app.route('/equipos/<id>' ,methods=['PUT'])
def update_equipo(id):
    equipo=Equipo.query.get(id)
    imagen=request.json['imagen']
    nombre=request.json['nombre']
    cantesc=request.json['cantesc']
    canttot=request.json['canttot']
    equipo.imagen=imagen
    equipo.nombre=nombre
    equipo.cantesc=cantesc
    equipo.canttot=canttot
    db.session.commit()
    return equipo_schema.jsonify(equipo)


 
# programa principal
if __name__=='__main__':  
    app.run(debug=True)  #, port=5000) 