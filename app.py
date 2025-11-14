from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def index():
    csv_path = 'mental_health_tech_survey.csv'
    
    try:
        # Ler CSV com encoding adequado
        try:
            df = pd.read_csv(csv_path, encoding='utf-8')
        except:
            df = pd.read_csv(csv_path, encoding='latin-1')
        
        # Limpar dados
        df = df.dropna(subset=['Age', 'treatment'])
        
        # Filtrar idades válidas (entre 18 e 75)
        df = df[(df['Age'] >= 18) & (df['Age'] <= 75)]
        
        # Selecionar apenas colunas relevantes para visualização
        colunas_relevantes = [
            'Age', 'Gender', 'Country', 'self_employed', 'family_history',
            'treatment', 'work_interfere', 'no_employees', 'remote_work',
            'tech_company', 'benefits', 'wellness_program', 'seek_help',
            'anonymity', 'leave', 'mental_health_consequence', 
            'coworkers', 'supervisor', 'mental_health_interview'
        ]
        
        # Verificar quais colunas existem no dataset
        colunas_existentes = [col for col in colunas_relevantes if col in df.columns]
        df_display = df[colunas_existentes].head(50)  # Mostrar primeiras 50 linhas
        
        # Converter para HTML
        table_html = df_display.to_html(
            classes='table table-striped table-hover table-sm', 
            index=False, 
            border=0
        )
        
        # Calcular estatísticas
        total_registros = len(df)
        
        stats = {
            'total': total_registros,
            'buscou_tratamento': len(df[df['treatment'] == 'Yes']) if 'treatment' in df.columns else 0,
            'historico_familiar': len(df[df['family_history'] == 'Yes']) if 'family_history' in df.columns else 0,
            'trabalho_interferido': len(df[df['work_interfere'].isin(['Often', 'Sometimes'])]) if 'work_interfere' in df.columns else 0,
            'empresa_tech': len(df[df['tech_company'] == 'Yes']) if 'tech_company' in df.columns else 0,
            'beneficios_sim': len(df[df['benefits'] == 'Yes']) if 'benefits' in df.columns else 0,
            'trabalho_remoto': len(df[df['remote_work'] == 'Yes']) if 'remote_work' in df.columns else 0,
            'idade_media': round(df['Age'].mean(), 1) if 'Age' in df.columns else 0,
            'paises_unicos': df['Country'].nunique() if 'Country' in df.columns else 0
        }
        
        # Calcular percentuais
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
                             colunas=colunas_existentes)
    
    except Exception as e:
        return f"""
        <div style="padding: 50px; text-align: center;">
            <h1>⚠️ Erro ao carregar CSV</h1>
            <p style="color: red; font-size: 18px;">{str(e)}</p>
            <hr>
            <h3>Instruções:</h3>
            <ol style="text-align: left; max-width: 600px; margin: 0 auto;">
                <li>Baixe o dataset do Kaggle: <a href="https://www.kaggle.com/datasets/osmi/mental-health-in-tech-survey" target="_blank">Mental Health in Tech Survey</a></li>
                <li>Renomeie o arquivo para: <code>mental_health_tech_survey.csv</code></li>
                <li>Coloque na pasta <code>data/</code> do projeto</li>
                <li>Faça commit e push para o GitHub</li>
            </ol>
        </div>
        """

if __name__ == '__main__':
    app.run(debug=True)
