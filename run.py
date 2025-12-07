from dotenv import load_dotenv
from app import create_app, db
from app.models import Project

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Project': Project}
