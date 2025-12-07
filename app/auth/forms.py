from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Usuário', 
                         validators=[DataRequired(message="Por favor, insira seu nome de usuário.")],
                         render_kw={"placeholder": "Nome de usuário"})
    password = PasswordField('Senha', 
                         validators=[DataRequired(message="Por favor, insira sua senha.")],
                         render_kw={"placeholder": "Senha"})
    remember_me = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')
