import os
import json
from flask import render_template, flash, redirect, url_for, current_app, request
from werkzeug.utils import secure_filename
from app import db
from app.admin import bp
from app.admin.forms import ProjectForm
from app.models import Project
from flask_login import login_required

def save_picture(form_picture_field):
    """Salva uma imagem do formulário no sistema de arquivos e retorna o caminho."""
    if form_picture_field and form_picture_field.data:
        picture_file = form_picture_field.data
        random_hex = os.urandom(8).hex()
        _, f_ext = os.path.splitext(picture_file.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(current_app.root_path, 'static/uploads', picture_fn)
        os.makedirs(os.path.dirname(picture_path), exist_ok=True)
        picture_file.save(picture_path)
        return f'uploads/{picture_fn}'
    return None

def process_dynamic_forms(project, form):
    """Processa e salva os dados dos formulários dinâmicos e das imagens a partir de um formulário validado."""
    # Popula os campos simples
    project.title = form.title.data
    project.description = form.description.data
    project.link = form.link.data
    project.detailed_description = form.detailed_description.data
    project.section2_title = form.section2_title.data
    project.section2_text = form.section2_text.data
    project.section3_title = form.section3_title.data
    project.section3_text = form.section3_text.data

    # Processa os uploads de imagem, apenas se um novo arquivo for enviado
    if form.image_file.data:
        project.image_filename = save_picture(form.image_file)
    if form.section2_image.data:
        project.section2_image = save_picture(form.section2_image)
    if form.section3_image.data:
        project.section3_image = save_picture(form.section3_image)

    # Filtra e serializa as listas dinâmicas para JSON
    # Apenas salva itens onde pelo menos um campo foi preenchido
    features_data = [item for item in form.features_grid.data if any(item.values())]
    accordion_data = [item for item in form.accordion_items.data if any(item.values())]
    stats_data = [item for item in form.stats_bar.data if any(item.values())]

    project.features_grid = json.dumps(features_data)
    project.accordion_items = json.dumps(accordion_data)
    project.stats_bar = json.dumps(stats_data)

@bp.route('/dashboard')
@login_required
def dashboard():
    projects = Project.query.all()
    return render_template('admin/dashboard.html', projects=projects, title='Painel Admin')

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project()
        process_dynamic_forms(project, form)
        db.session.add(project)
        db.session.commit()
        flash('Seu projeto foi adicionado com sucesso!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/project_form.html', title='Adicionar Projeto', form=form, legend='Novo Projeto')

@bp.route('/edit/<int:project_id>', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    form = ProjectForm()

    # Se o formulário for submetido e válido (POST request)
    if form.validate_on_submit():
        process_dynamic_forms(project, form)
        db.session.commit()
        flash('Seu projeto foi atualizado com sucesso!', 'success')
        return redirect(url_for('admin.dashboard'))

    # Se a página for carregada pela primeira vez (GET request)
    elif request.method == 'GET':
        # Popula campos simples
        form.title.data = project.title
        form.description.data = project.description
        form.link.data = project.link
        form.detailed_description.data = project.detailed_description
        form.section2_title.data = project.section2_title
        form.section2_text.data = project.section2_text
        form.section3_title.data = project.section3_title
        form.section3_text.data = project.section3_text
        
        # Popula os campos FieldList a partir do JSON
        if project.features_grid:
            for item in json.loads(project.features_grid):
                form.features_grid.append_entry(item)
        if project.accordion_items:
            for item in json.loads(project.accordion_items):
                form.accordion_items.append_entry(item)
        if project.stats_bar:
            for item in json.loads(project.stats_bar):
                form.stats_bar.append_entry(item)

    # Renderiza o template. Se for um GET, o formulário estará populado.
    # Se for um POST inválido, o WTForms irá repopular os campos com os dados submetidos e exibir os erros.
    return render_template('admin/project_form.html', title='Editar Projeto', form=form, legend=f'Editando "{project.title}"')

@bp.route('/delete/<int:project_id>', methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash('Projeto excluído com sucesso.', 'success')
    return redirect(url_for('admin.dashboard'))
