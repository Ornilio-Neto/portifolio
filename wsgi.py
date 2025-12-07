from dotenv import load_dotenv
import os

# Caminho para o diretório do projeto
project_folder = os.path.expanduser('~/meu-portfolio') # <- IMPORTANTE: Mude 'meu-portfolio' para o nome da sua pasta no PythonAnywhere
load_dotenv(os.path.join(project_folder, '.env'))

from run import app as application
