from app import db
from flask_login import UserMixin

# Modelo do Projeto para o Banco de Dados
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(200))
    image_filename = db.Column(db.String(120), nullable=False)
    detailed_description = db.Column(db.Text)
    
    # Campos para conteúdo dinâmico (armazenados como JSON)
    features_grid = db.Column(db.Text)
    accordion_items = db.Column(db.Text)
    stats_bar = db.Column(db.Text)
    
    # Campos para seções adicionais
    section2_title = db.Column(db.String(100))
    section2_text = db.Column(db.Text)
    section2_image = db.Column(db.String(120))

    section3_title = db.Column(db.String(100))
    section3_text = db.Column(db.Text)
    section3_image = db.Column(db.String(120))

    def __repr__(self):
        return f'<Project {self.title}>'


# Modelo de Usuário para o Login
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def check_password(self, password):
        # Em um app real, aqui você usaria werkzeug.security.check_password_hash
        return self.password == password

# --- USUÁRIO ADMINISTRADOR FIXO ---
# Em uma aplicação real, isso viria de um banco de dados de usuários.
admin_user = User(id='1', username='admin', password='password')

# Dicionário para simular a busca de usuários pelo ID, usado pelo Flask-Login
users = {admin_user.id: admin_user}
