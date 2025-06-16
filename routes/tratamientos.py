from flask import Blueprint, request, jsonify, current_app

tratamientos_bp = Blueprint('tratamientos', __name__)


# Registrar nuevo tratamiento
@tratamientos_bp.route('/registroTratamiento', methods=['POST'])
def registroTratamiento():
    datos = request.get_json()

    if not datos or not all(k in datos for k in ("nombre", "descripcion", "categoria")):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    con = current_app.mysql.connection.cursor()
    con.execute("""
        INSERT INTO tratamientos (nombre, descripcion, categoria)
        VALUES (%s, %s, %s)
    """, (datos["nombre"], datos["descripcion"], datos["categoria"]))
    current_app.mysql.connection.commit()
    return jsonify({"mensaje": "Tratamiento registrado"})


# Editar tratamiento existente
@tratamientos_bp.route('/editarTratamiento/<int:id>', methods=['PUT'])
def editarTratamiento(id):
    datos = request.get_json()

    if not datos or not all(k in datos for k in ("nombre", "descripcion", "categoria")):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    con = current_app.mysql.connection.cursor()
    con.execute("""
        UPDATE tratamientos
        SET nombre=%s, descripcion=%s, categoria=%s
        WHERE id=%s
    """, (datos["nombre"], datos["descripcion"], datos["categoria"], id))
    current_app.mysql.connection.commit()
    return jsonify({"mensaje": "Tratamiento actualizado"})


# Eliminar tratamiento
@tratamientos_bp.route('/eliminarTratamiento/<int:id>', methods=['DELETE'])
def eliminarTratamiento(id):
    con = current_app.mysql.connection.cursor()
    con.execute("DELETE FROM tratamientos WHERE id = %s", (id,))
    current_app.mysql.connection.commit()
    return jsonify({"mensaje": "Tratamiento eliminado"})


# Listar tratamientos
@tratamientos_bp.route('/listadoTratamientos', methods=['GET'])
def listadoTratamientos():
    con = current_app.mysql.connection.cursor()
    con.execute("SELECT id, nombre, descripcion, categoria FROM tratamientos")
    tratamientos = con.fetchall()

    listado = []
    for t in tratamientos:
        listado.append({
            "id": t[0],
            "nombre": t[1],
            "descripcion": t[2],
            "categoria": t[3]
        })

    return jsonify(listado)