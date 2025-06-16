from .usuarios import usuarios_bp
from .citas import citas_bp
from .tratamientos import tratamientos_bp
from .documentacion import documentacion_bp

def registrar_rutas(app):
    app.register_blueprint(usuarios_bp, url_prefix  ='/usuarios')
    app.register_blueprint(citas_bp, url_prefix ='/citas')
    app.register_blueprint(tratamientos_bp, url_prefix ='/tratamientos')
    app.register_blueprint(documentacion_bp, url_prefix ='/documentacion')