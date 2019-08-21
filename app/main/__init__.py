from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from app.main.model import revoked_token_model


from .config import config_by_name

db = SQLAlchemy()
flask_bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    JWTManager.init_app(app)

    return app

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return model.revoked_token_model.is_jti_blacklisted(jti)