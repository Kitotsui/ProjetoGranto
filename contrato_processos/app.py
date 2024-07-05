from flask import Flask, render_template, request, redirect, url_for, session
from flask_bootstrap import Bootstrap
import spacy
import fitz
import re
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'
Bootstrap(app)

nlp = spacy.load("pt_core_news_sm")

# Expressões regulares para captura de diferentes padrões
regex_patterns = {
    "DATAS": r"\b\d{1,2}/\d{1,2}/\d{2,4}\b|\b\d{4}/\d{4}\b|\b\d{3}/\d{3}\b|\bXXXX/\d{4}\b|\bXXX/\d{4}\b",
    "VALOR": r"R\$\s?[\d\.,]+(\s?\([\w\s]+\))?",
    "CNPJ": r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b",
    "CPF": r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b",
    "RG": r"RG n.\s?\d{1,2}\.\d{3}\.\d{3}-\d{1}\b",
    "TELEFONES": r"\b\(?\d{2}\)?\s?\d{4,5}-\d{4}\b",
    "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    "NUMEROS DE CONTRATO": r"CONTRATO N.\s?\d+|\bConcorrência n.\s?\d+\b",
    "NOMES DE EMPRESA": r"((?:[A-Z][a-z]+\s?)+\b\S*[A-Z]{2,}\S*)",
    "NUMEROS DE DOCUMENTO": r"doc.\s?SEI n.\s?\d{6,}",
    "NUMEROS DO SEI": r"SEI n.\s?\d{10}",
    "DOTACAO ORCAMENTARIA": r"dotação orçamentária n.\s?\d{23}",
    "LOCALIZACAO": r"Rua\s[\w\s,]+",
    "NOMES DE PESSOAS": r"Sr.\s[\w\s]+"
}

# Função para extrair informações usando expressões regulares
def extract_info(text):
    extracted_data = {key: re.findall(pattern, text) for key, pattern in regex_patterns.items()}
    return extracted_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/leitura_contratos')
def leitura_contratos():
    return render_template('leitura_contratos.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename

        pdf_document = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text += page.get_text()

        doc = nlp(text)
        extracted_data = extract_info(text)

        for ent in doc.ents:
            label = ent.label_
            if label == 'LOC':
                label = 'Localização'
            elif label == 'PER':
                label = 'Nomes de pessoas'
            elif label == 'ORG':
                label = 'Nomes de Organizações'
            if label in extracted_data:
                extracted_data[label].append(ent.text)
            else:
                extracted_data[label] = [ent.text]

        #removi o misc e mudei a ordem das chaces q aparecem no result
        for key in list(extracted_data.keys()):
            if key not in ["DATAS", "VALOR", "CNPJ", "CPF", "RG", "TELEFONES", "EMAIL", "NUMEROS DE CONTRATO", "NOMES DE EMPRESA", "LOCALIZAÇÃO", "NOMES DE PESSOAS", "NOMES DE ORGANIZAÇÕES", "NÚMEROS DE DOCUMENTO", "NÚMEROS DO SEI", "DOTACÃO ORÇAMENTARIA"]:
                del extracted_data[key]

        processed_data = {
            "filename": filename,
            **extracted_data
        }

        print("Dados processados:", processed_data)

        session['processed_data'] = json.dumps(processed_data)

        return redirect(url_for('result'))

@app.route('/result')
def result():
    result = json.loads(session.get('processed_data', '{}'))
    print("Dados recuperados da sessão:", result)
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
