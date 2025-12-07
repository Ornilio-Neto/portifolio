from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
# Importar o Form simples do WTForms
from wtforms import StringField, TextAreaField, SubmitField, FormField, FieldList, Form
from wtforms.validators import DataRequired, Length, Optional

# --- Mini-formulários para os itens das listas dinâmicas ---
# Alterado de FlaskForm para Form
class FeatureForm(Form):
    """Sub-formulário para uma única funcionalidade."""
    title = StringField('Título da Funcionalidade', validators=[Optional(), Length(max=100)])
    description = TextAreaField('Descrição da Funcionalidade', validators=[Optional()])

# Alterado de FlaskForm para Form
class AccordionItemForm(Form):
    """Sub-formulário para um único item de acordeão."""
    title = StringField('Título (Pergunta)', validators=[Optional(), Length(max=200)])
    content = TextAreaField('Conteúdo (Resposta)', validators=[Optional()])

# Alterado de FlaskForm para Form
class StatForm(Form):
    """Sub-formulário para uma única estatística."""
    value = StringField('Valor', validators=[Optional(), Length(max=50)])
    label = StringField('Rótulo', validators=[Optional(), Length(max=100)])


# --- Formulário Principal do Projeto (Este continua como FlaskForm) ---

class ProjectForm(FlaskForm):
    # --- Informações para o card do portfólio ---
    title = StringField('Título do Projeto', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Descrição Curta (para o card)', validators=[DataRequired()])
    image_file = FileField('Imagem Principal (Thumbnail)', validators=[FileAllowed(['jpg', 'png', 'gif'], 'Apenas imagens!')])
    link = StringField('Link do Projeto', validators=[Optional(), Length(max=200)])

    # --- Conteúdo completo da página de detalhes ---
    detailed_description = TextAreaField('Descrição Detalhada (Seção 1)', validators=[Optional()])

    # Seção 2: Bloco de texto e imagem 1
    section2_title = StringField('Título da Seção 2', validators=[Optional(), Length(max=200)])
    section2_text = TextAreaField('Texto da Seção 2', validators=[Optional()])
    section2_image = FileField('Imagem da Seção 2', validators=[FileAllowed(['jpg', 'png', 'gif'], 'Apenas imagens!')])

    # Seção 3: Bloco de texto e imagem 2
    section3_title = StringField('Título da Seção 3', validators=[Optional(), Length(max=200)])
    section3_text = TextAreaField('Texto da Seção 3', validators=[Optional()])
    section3_image = FileField('Imagem da Seção 3', validators=[FileAllowed(['jpg', 'png', 'gif'], 'Apenas imagens!')])

    # --- Seções Dinâmicas (Substituindo os campos JSON) ---
    features_grid = FieldList(FormField(FeatureForm), min_entries=0, label="Grade de Funcionalidades")
    accordion_items = FieldList(FormField(AccordionItemForm), min_entries=0, label="Itens do Acordeão (FAQ)")
    stats_bar = FieldList(FormField(StatForm), min_entries=0, label="Barra de Estatísticas")

    submit = SubmitField('Salvar Projeto')
