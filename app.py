from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/display', methods=['POST'])
def display_file():
    file = request.files['file']
    if not file:
        return "No file"
    
    # Tenta ler o arquivo com diferentes codificações
    try:
        df = pd.read_csv(file, delimiter=";")
    except UnicodeDecodeError:
        file.seek(0)
        try:
            df = pd.read_csv(file, encoding='latin1', delimiter=";")
        except UnicodeDecodeError:
            file.seek(0)
            df = pd.read_csv(file, encoding='ISO-8859-1', delimiter=";")
    
    return render_template('display.html', 
                         tables=[df.to_html(classes='data')], 
                         titles=df.columns.values)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=False, host='0.0.0.0', port=port)
