from flask import Blueprint, request, jsonify, current_app

usuarios_bp = Blueprint('usuarios', __name__)


# iniciar sesión (login)
@usuarios_bp.route('/login', methods=['POST'])
def login():
    datos = request.get_json()
    correo = datos.get("correo")
    contrasena_ingresada = datos.get("contrasena")

    con = current_app.mysql.connection.cursor()
    con.execute("SELECT id, nombre, contrasena FROM usuarios WHERE correo = %s", (correo,))
    usuario = con.fetchone()

    if usuario and contrasena_ingresada == usuario[2]:
        return jsonify({
            "mensaje": "Login exitoso",
            "usuario": {
                "id": usuario[0],
                "nombre": usuario[1]
            }
        })
    else:
        return jsonify({"mensaje": "Credenciales incorrectas"}), 401
    

# listar todos los pacientes registrados
@usuarios_bp.route('/listadoPacientes', methods=['GET'])
def listar_usuarios():
    con = current_app.mysql.connection.cursor()
    con.execute("SELECT * FROM usuarios")
    pacientes = con.fetchall()
    listado = []

    for paciente in pacientes:
        listado.append({
            "id": paciente[0],
            "nombre": paciente[1],
            "apellido": paciente[2],
            "cedula": paciente[3],
            "telefono": paciente[4],
            "correo": paciente[5],
            "direccion": paciente[6],
            "fecha_registro": paciente[7],
        })

    return jsonify(pacientes)


# registrar un nuevo paciente
@usuarios_bp.route('/registroPaciente', methods=['POST'])
def registroPaciente():
    datos = request.get_json()

    contrasena_plana = datos.get("contrasena", "")

    con = current_app.mysql.connection.cursor()
    con.execute("""
        INSERT INTO usuarios (nombre, apellido, cedula, telefono, correo, direccion, fecha_registro, contrasena)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        datos["nombre"], datos["apellido"], datos["cedula"], datos["telefono"],
        datos["correo"], datos["direccion"], datos["fecha_registro"], contrasena_plana
    ))
    current_app.mysql.connection.commit()
    return jsonify({"mensaje": "Paciente registrado con contraseña"})


# editar los datos de un paciente 
@usuarios_bp.route('/editarPaciente/<int:id>', methods=['PUT'])
def editarPaciente(id):
    datos = request.get_json()
    con = current_app.mysql.connection.cursor()
    con.execute("""
        UPDATE usuarios SET nombre=%s, apellido=%s, telefono=%s, correo=%s, direccion=%s
        WHERE id=%s
    """, (datos["nombre"], datos["apellido"], datos["telefono"],
          datos["correo"], datos["direccion"], id))
    current_app.mysql.connection.commit()
    return jsonify({"mensaje": "Paciente actualizado"})


# eliminar un paciente
@usuarios_bp.route('/eliminarPaciente/<int:id>', methods=['DELETE'])
def eliminarPaciente(id):
    con = current_app.mysql.connection.cursor()
    con.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    current_app.mysql.connection.commit()
    return jsonify({"mensaje": "Paciente eliminado"})