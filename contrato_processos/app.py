from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap4
import spacy
import json

app = Flask(__name__)
Bootstrap4(app)

# Carregar o modelo do SpaCy
nlp = spacy.load("pt_core_news_sm")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        text = file.read().decode('utf-8')
        doc = nlp(text)
        # Processamento de texto
        # Adicione a lógica de extração aqui
        processed_data = {
            "cnpjs": ["12.345.678/0001-90"],
            "valores": ["R$ 500.000,00"],
            "classificacao": ["Tecnologia, desenvolvimento, suporte técnico"],
            "empresa_contratante": "TechSoluções S.A.",
            "empresa_contratada": "Soluções Rápidas Ltda.",
            "vigencia_contrato": "01/07/2024 a 30/06/2025"
        }
        return redirect(url_for('result', result=json.dumps(processed_data)))

@app.route('/result')
def result():
    result = json.loads(request.args.get('result'))
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
