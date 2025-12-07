from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app.auth import bp
from app.auth.forms import LoginForm
from app.models import users, admin_user

@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Se o usuário já estiver autenticado, redireciona para a home
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        # Verifica se o usuário existe e a senha está correta
        user = users.get('1') # Pega o nosso admin user
        if user and user.check_password(form.password.data) and user.username == form.username.data:
            login_user(user, remember=form.remember_me.data)
            flash('Login realizado com sucesso!', 'success')
            
            # Redireciona para a próxima página ou para o dashboard do admin
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin.dashboard'))
        else:
            flash('Credenciais inválidas. Por favor, tente novamente.', 'danger')

    return render_template('auth/login.html', title='Login', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
