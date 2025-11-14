from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
app.config['UPLOAD_FOLDER'] = 'uploads'

# Criar pasta de uploads se não existir
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    csv_path = os.path.join('data', 'mental_health_tech_survey.csv')
    
    try:
        try:
            df = pd.read_csv(csv_path, encoding='utf-8')
        except:
            df = pd.read_csv(csv_path, encoding='latin-1')
        
        df = df.dropna(subset=['Age', 'treatment'])
        df = df[(df['Age'] >= 18) & (df['Age'] <= 75)]
        
        colunas_relevantes = [
            'Age', 'Gender', 'Country', 'self_employed', 'family_history',
            'treatment', 'work_interfere', 'no_employees', 'remote_work',
            'tech_company', 'benefits', 'wellness_program', 'seek_help',
            'anonymity', 'leave', 'mental_health_consequence', 
            'coworkers', 'supervisor', 'mental_health_interview'
        ]
        
        colunas_existentes = [col for col in colunas_relevantes if col in df.columns]
        df_display = df[colunas_existentes].head(50)
        
        table_html = df_display.to_html(
            classes='table table-striped table-hover table-sm', 
            index=False, 
            border=0
        )
        
        total_registros = len(df)
        
        stats = {
            'total': total_registros,
            'buscou_tratamento': len(df[df['treatment'] == 'Yes']) if 'treatment' in df.columns else 0,
            'historico_familiar': len(df[df['family_history'] == 'Yes']) if 'family_history' in df.columns else 0,
            'trabalho_interferido': len(df[df['work_interfere'].isin(['Often', 'Sometimes'])]) if 'work_interfere' in df.columns else 0,
            'empresa_tech': len(df[df['tech_company'] == 'Yes']) if 'tech_company' in df.columns else 0,
            'beneficios_sim': len(df[df['benefits'] == 'Yes']) if 'benefits' in df.columns else 0,
            'trabalho_remoto': len(df[df['remote_work'] == 'Yes']) if 'remote_work' in df.columns else 0,
            'paises_unicos': df['Country'].nunique() if 'Country' in df.columns else 0
        }
        
        percentuais = {
            'perc_tratamento': round((stats['buscou_tratamento'] / total_registros) * 100, 1),
            'perc_historico': round((stats['historico_familiar'] / total_registros) * 100, 1),
            'perc_interferencia': round((stats['trabalho_interferido'] / total_registros) * 100, 1),
            'perc_beneficios': round((stats['beneficios_sim'] / total_registros) * 100, 1) if stats['total'] > 0 else 0
        }
        
        return render_template('index.html', 
                             table=table_html, 
                             stats=stats,
                             percentuais=percentuais,
                             colunas=colunas_existentes,
                             show_upload=True)
    
    except Exception as e:
        return f"<h1>Erro: {str(e)}</h1><p>Verifique se o arquivo CSV está na pasta data/</p>"

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Verificar se o arquivo foi enviado
        if 'file' not in request.files:
            return render_template('upload.html', error='Nenhum arquivo selecionado')
        
        file = request.files['file']
        
        if file.filename == '':
            return render_template('upload.html', error='Nenhum arquivo selecionado')
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Redirecionar para visualização
            return redirect(url_for('view_csv', filename=filename))
        else:
            return render_template('upload.html', error='Apenas arquivos CSV são permitidos')
    
    return render_template('upload.html')

@app.route('/view/<filename>')
def view_csv(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(filepath):
        return "<h1>Arquivo não encontrado</h1>"
    
    try:
        # Tentar diferentes encodings
        try:
            df = pd.read_csv(filepath, encoding='utf-8')
        except:
            try:
                df = pd.read_csv(filepath, encoding='latin-1')
            except:
                df = pd.read_csv(filepath, encoding='iso-8859-1')
        
        # Limitar a 1000 linhas para performance
        if len(df) > 1000:
            df_display = df.head(1000)
            truncated = True
        else:
            df_display = df
            truncated = False
        
        # Converter para HTML
        table_html = df_display.to_html(
            classes='table table-striped table-hover table-sm', 
            index=False, 
            border=0
        )
        
        # Informações do CSV
        csv_info = {
            'filename': filename,
            'total_linhas': len(df),
            'total_colunas': len(df.columns),
            'colunas': list(df.columns),
            'truncated': truncated
        }
        
        return render_template('view_csv.html', 
                             table=table_html,
                             info=csv_info)
    
    except Exception as e:
        return f"<h1>Erro ao ler o arquivo</h1><p>{str(e)}</p><p>Verifique se o arquivo é um CSV válido.</p>"

if __name__ == '__main__':
    app.run(debug=True)
