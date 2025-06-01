from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__, template_folder='templates')
app.secret_key = 'una_clave_secreta_muy_segura_123456'

client = MongoClient('mongodb+srv://geraldandrade9706:8709729@cluster0.udflfjm.mongodb.net/')
db = client['LoginAPI']
usuarios_collection = db['usuarios']
peliculas_collection = db['peliculas']

def obtener_peliculas_desde_bd():
    peliculas = list(peliculas_collection.find())
    for p in peliculas:
        p['_id'] = str(p['_id'])
    return peliculas

@app.route('/')
def formulario_registro():
    return render_template('registro.html')

@app.route('/login', methods=['GET'])
def mostrar_login():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json(force=True)
    nombre = data.get('nombre')
    correo = data.get('correo')
    usuario = data.get('usuario')
    contraseña = data.get('contraseña')

    if usuarios_collection.find_one({"usuario": usuario}):
        return jsonify({"mensaje": "El usuario ya existe"}), 400

    usuarios_collection.insert_one({
        "nombre": nombre,
        "correo": correo,
        "usuario": usuario,
        "contraseña": contraseña,
        "favoritas": [],
        "carrito_renta": []
    })

    return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    correo = data.get('correo')
    contraseña = data.get('contraseña')

    if correo == 'admin@admin.com' and contraseña == 'admin':
        session['admin_logged_in'] = True
        session.pop('user_logged_in', None)
        session.pop('correo_usuario', None)
        return jsonify({'success': True, 'admin': True})

    usuario = usuarios_collection.find_one({'correo': correo, 'contraseña': contraseña})
    if usuario:
        session['user_logged_in'] = True
        session['correo_usuario'] = correo
        session.pop('admin_logged_in', None)
        return jsonify({'success': True, 'admin': False})

    return jsonify({'success': False, 'mensaje': 'Correo o contraseña incorrectos'}), 401

@app.route('/bienvenida')
def bienvenida():
    if session.get('user_logged_in'):
        peliculas = obtener_peliculas_desde_bd()
        return render_template('bienvenida.html', peliculas=peliculas)
    else:
        return redirect(url_for('mostrar_login'))

@app.route('/admin')
def admin():
    if session.get('admin_logged_in'):
        peliculas = obtener_peliculas_desde_bd()
        return render_template('admin.html', peliculas=peliculas)
    else:
        return redirect(url_for('mostrar_login'))

@app.route('/admin/agregar_pelicula', methods=['POST'])
def agregar_pelicula():
    if not session.get('admin_logged_in'):
        return jsonify({'mensaje': 'Acceso denegado'}), 403

    data = request.get_json(force=True)
    titulo = data.get('titulo')
    año = data.get('año')
    genero = data.get('genero')
    director = data.get('director')
    poster_base64 = data.get('poster')
    precio = float(data.get('precio', 0.0))

    if not all([titulo, año, genero, director, poster_base64]):
        return jsonify({'mensaje': 'Faltan datos obligatorios'}), 400

    pelicula = {
        "titulo": titulo,
        "año": int(año),
        "genero": genero,
        "director": director,
        "poster": poster_base64,
        "precio": precio,
        "rentada_por": None
    }

    peliculas_collection.insert_one(pelicula)
    return jsonify({'mensaje': 'Película agregada exitosamente'}), 201

@app.route('/peliculas', methods=['GET'])
def ver_peliculas():
    if not session.get('user_logged_in') and not session.get('admin_logged_in'):
        return redirect(url_for('mostrar_login'))

    peliculas = obtener_peliculas_desde_bd()
    return render_template('peliculas.html', peliculas=peliculas)

@app.route('/usuario/favorita/<pelicula_id>', methods=['POST'])
def guardar_favorita(pelicula_id):
    if not session.get('user_logged_in'):
        return jsonify({'mensaje': 'No autorizado'}), 401

    correo = session.get('correo_usuario')
    usuario = usuarios_collection.find_one({'correo': correo})
    if not usuario:
        return jsonify({'mensaje': 'Usuario no encontrado'}), 404

    try:
        pelicula_objid = ObjectId(pelicula_id)
    except:
        return jsonify({'mensaje': 'ID inválido'}), 400

    pelicula = peliculas_collection.find_one({'_id': pelicula_objid})
    if not pelicula:
        return jsonify({'mensaje': 'Película no encontrada'}), 404

    favoritas = usuario.get('favoritas', [])
    if pelicula_id not in favoritas:
        favoritas.append(pelicula_id)
        usuarios_collection.update_one({'correo': correo}, {'$set': {'favoritas': favoritas}})

    return jsonify({'mensaje': 'Película añadida como favorita'})

@app.route('/usuario/rentar/<pelicula_id>', methods=['POST'])
def rentar_pelicula(pelicula_id):
    if not session.get('user_logged_in'):
        return jsonify({'mensaje': 'No autorizado'}), 401

    correo = session.get('correo_usuario')
    usuario = usuarios_collection.find_one({'correo': correo})
    if not usuario:
        return jsonify({'mensaje': 'Usuario no encontrado'}), 404

    try:
        pelicula_objid = ObjectId(pelicula_id)
    except:
        return jsonify({'mensaje': 'ID inválido'}), 400

    pelicula = peliculas_collection.find_one({'_id': pelicula_objid})
    if not pelicula:
        return jsonify({'mensaje': 'Película no encontrada'}), 404

    # Verificar si ya está rentada
    if pelicula.get('rentada_por'):
        return jsonify({'mensaje': 'Película ya rentada por otro usuario'}), 403

    # Verificar si está en carrito de otro usuario
    pelicula_id_str = str(pelicula_objid)
    otra_persona_con_carrito = usuarios_collection.find_one({
        'carrito_renta': pelicula_id_str,
        'correo': {'$ne': correo}
    })
    if otra_persona_con_carrito:
        return jsonify({'mensaje': 'Película ya está en el carrito de otro usuario'}), 403

    usuarios_collection.update_one(
        {'correo': correo},
        {'$addToSet': {'carrito_renta': pelicula_id_str}}
    )

    return jsonify({'mensaje': 'Película añadida al carrito de renta'})

@app.route('/usuario/rentar/eliminar/<pelicula_id>', methods=['POST'])
def eliminar_de_factura(pelicula_id):
    if not session.get('user_logged_in'):
        return jsonify({'mensaje': 'No autorizado'}), 401

    correo = session.get('correo_usuario')
    usuarios_collection.update_one({'correo': correo}, {'$pull': {'carrito_renta': pelicula_id}})
    return jsonify({'mensaje': 'Película eliminada del carrito'}), 200

@app.route('/usuario/rentar/resumen', methods=['GET'])
def factura():
    if not session.get('user_logged_in'):
        return redirect(url_for('mostrar_login'))

    correo = session.get('correo_usuario')
    usuario = usuarios_collection.find_one({'correo': correo})

    carrito_ids = usuario.get('carrito_renta', [])
    peliculas_renta = []
    total = 0.0

    for id_str in carrito_ids:
        pelicula = peliculas_collection.find_one({'_id': ObjectId(id_str)})
        if pelicula and not pelicula.get('rentada_por'):
            pelicula['_id'] = str(pelicula['_id'])  # importante para usar en HTML
            peliculas_renta.append(pelicula)
            total += pelicula.get('precio', 0.0)

    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    return render_template('factura.html', peliculas=peliculas_renta, total=round(total, 2), usuario=usuario, fecha=fecha_actual)

@app.route('/usuario/rentar/confirmar', methods=['POST'])
def confirmar_renta():
    if not session.get('user_logged_in'):
        return jsonify({'mensaje': 'No autorizado'}), 401

    correo = session.get('correo_usuario')
    usuario = usuarios_collection.find_one({'correo': correo})
    carrito_ids = usuario.get('carrito_renta', [])

    for id_str in carrito_ids:
        peliculas_collection.update_one(
            {'_id': ObjectId(id_str), 'rentada_por': None},
            {'$set': {'rentada_por': correo}}
        )

    usuarios_collection.update_one({'correo': correo}, {'$set': {'carrito_renta': []}})

    return jsonify({'mensaje': 'Renta confirmada correctamente'})

if __name__ == '__main__':
    app.run(debug=True)
