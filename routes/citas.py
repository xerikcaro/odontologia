from flask import Blueprint, request, jsonify, current_app

citas_bp = Blueprint('citas', __name__)


# registrar una nueva cita médica
@citas_bp.route('/registroCita', methods=['POST'])
def registrarCita():
    datos = request.get_json()

    if not datos or not all(k in datos for k in ("paciente_id", "fecha", "hora", "motivo", "observaciones")):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    con = current_app.mysql.connection.cursor()
    con.execute("""
        INSERT INTO citas (paciente_id, fecha, hora, motivo, observaciones)
        VALUES (%s, %s, %s, %s, %s)
    """, (datos["paciente_id"], datos["fecha"], datos["hora"], datos["motivo"], datos["observaciones"]))
    current_app.mysql.connection.commit()
    return jsonify({"mensaje": "Cita registrada"})


# editar una cita existente
@citas_bp.route('/editarCita/<int:id>', methods=['PUT'])
def editarCita(id):
    datos = request.get_json()

    campos_requeridos = ("fecha", "hora", "motivo", "observaciones")
    if not datos or not all(k in datos for k in campos_requeridos):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    con = current_app.mysql.connection.cursor()
    con.execute("""
        UPDATE citas
        SET fecha=%s, hora=%s, motivo=%s, observaciones=%s
        WHERE id=%s
    """, (datos["fecha"], datos["hora"], datos["motivo"], datos["observaciones"], id))
    current_app.mysql.connection.commit()
    return jsonify({"mensaje": "Cita actualizada"})


# eliminar una cita
@citas_bp.route('/eliminarCita/<int:id>', methods=['DELETE'])
def eliminarCita(id):
    con = current_app.mysql.connection.cursor()
    con.execute("DELETE FROM citas WHERE id = %s", (id,))
    current_app.mysql.connection.commit()
    return jsonify({"mensaje": "Cita eliminada"})


# citas registradas
@citas_bp.route('/listadoCitas')
def listadoCitas():
    con = current_app.mysql.connection.cursor()
    con.execute("""
        SELECT 
            citas.id, 
            citas.fecha, 
            citas.hora, 
            citas.motivo, 
            citas.observaciones, 
            citas.paciente_id
        FROM citas
    """)
    citas = con.fetchall()

    listado = []
    for cita in citas:
        listado.append({
            "id": cita[0],
            "fecha": str(cita[1]),
            "hora": str(cita[2]),
            "motivo": cita[3],
            "observaciones": cita[4],
            "paciente_id": cita[5]
        })

    return jsonify(listado)