import sys
import os
from dotenv import load_dotenv

# Adiciona o diretório do projeto ao path do Python
project_folder = os.path.expanduser('~/portifolio')
if project_folder not in sys.path:
    sys.path.insert(0, project_folder)

# Carrega as variáveis de ambiente
load_dotenv(os.path.join(project_folder, '.env'))

from run import app as application
