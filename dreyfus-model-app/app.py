from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

import config
from models import db
from services import api_bp


def create_app():
    app = Flask(__name__)
    CORS(app)
    jwt = JWTManager(app)
    print(config.SQLALCHEMY_DATABASE_URI)
    app.config["SECRET_KEY"] = config.SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
    app.config["CORS_HEADERS"] = "Content-Type"

    db.init_app(app)
    app.register_blueprint(api_bp)

    with app.app_context():
        db.create_all()

    Migrate(app, db)

    print(app.url_map)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=8001)