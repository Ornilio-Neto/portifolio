from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, faça o login para acessar esta página.'
login_manager.login_message_category = 'info'

from .models import users
@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # --- LINHA DE DIAGNÓSTICO ---
    # Imprime a chave que o Flask está usando no Server Log.
    print(f"--- DIAGNOSTICO FLASK: A SECRET_KEY utilizada é: {app.config.get('SECRET_KEY')} ---", flush=True)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.main import bp as main_bp
    from app.admin import bp as admin_bp
    from app.auth import bp as auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    with app.app_context():
        from . import models

    return app
