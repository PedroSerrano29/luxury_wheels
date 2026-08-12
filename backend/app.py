from flask import Flask
from config import Config
from models import db
from routes.veiculos import veiculos_bp
from routes.auth import clientes_bp
from routes.reservas import reserva_bd

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    app.register_blueprint(veiculos_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(reserva_bd)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)