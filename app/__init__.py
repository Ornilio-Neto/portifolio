from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login' # Define a rota de login
login_manager.login_message = 'Por favor, faça o login para acessar esta página.'
login_manager.login_message_category = 'info'

# Função que o Flask-Login usará para carregar um usuário a partir do ID
from .models import users
@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app) # Inicializa o LoginManager para o app

    # Importar Blueprints
    from app.main import bp as main_bp
    from app.admin import bp as admin_bp
    from app.auth import bp as auth_bp # Importar o novo blueprint

    # Registrar Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth') # Registrar o blueprint

    with app.app_context():
        from . import models

    return app
