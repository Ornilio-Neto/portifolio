import json
from flask import render_template, abort
from app.main import bp
from app.models import Project

# Função auxiliar para carregar JSON de forma segura
def load_json(data, default=None):
    if not data:
        return default or []
    try:
        return json.loads(data)
    except (json.JSONDecodeError, TypeError):
        return default or []

# Rota principal (landing page)
@bp.route('/')
def index():
    return render_template('landing.html', title='Home')

# Rota para a lista de projetos
@bp.route('/portfolio')
def portfolio():
    projects = Project.query.order_by(Project.id.desc()).all()
    return render_template('index.html', projects=projects, title='Portfólio')

# Rota para exibir os detalhes de um projeto específico
@bp.route('/project/<int:project_id>')
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    
    # Carrega os dados JSON dos campos de texto para o template
    features = load_json(project.features_grid)
    accordion = load_json(project.accordion_items)
    stats = load_json(project.stats_bar)
    
    return render_template(
        'project_detail.html', 
        title=project.title, 
        project=project,
        features=features,
        accordion=accordion,
        stats=stats
    )
