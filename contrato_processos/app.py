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
    #padrão pra datas normais: \b\d{1,2}/\d{1,2}/\d{2,4}\b
    "DATAS": r"\b\d{4}/\d{4}\b|\b\d{3}/\d{3}\b|\bXXXX/\d{4}\b|\bXXX/\d{4}\b|\bdata-base de XXXX/2023\b|\bdata-base de \d{4}/2023\b|\bSão Paulo, XX de mês de 2023\b|\bSão Paulo, \d{2} de mês de 2023\b",
    "VALOR": r"R\$\s?[\d\.,]+.*?\)|R\$ [X\s\.,]+\([X]+\)|R\$ [X\.\,]+ \(por extenso\)|R\$ [X\.\,]+ \(POR EXTENSO\)",
    "CNPJ": r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b|\b CNPJ/MF sob n. XXXXXXXXXXXXXX\b",
    "DOCUMENTOS": r"RG n.\s?\d{1,2}\.\d{3}\.\d{3}-\d{1}\b|\b\d{3}\.\d{3}\.\d{3}-\d{2}\b|\b CPF/MF n. XXXXXXXXXX\b|\b RG n. XXXXXXXXX\b",
    "TELEFONES": r"\b\(?\d{2}\)?\s?\d{4,5}-\d{4}\b|\bTelefones?: \(\d{2}\) \d{4,5}-\d{4}|\bTelefones: \(XX\) XXXX-XXXX\b",
    "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b|\bE\-?mail: XXXXXXXXXXXXXXXXXXXXXX\b",
    "NUMEROS DE CONTRATO": r"CONTRATO N.\s?\d+|\bConcorrência n.\s?\d+\b|\bCONTRATO N.\s?XXX/[A-Z]+/\d{4}\b|\b Concorrência n. \s?XXX/[A-Z]+/\d{4}\b",
    "NOMES DE EMPRESA": r"((?:[A-Z][a-z]+\s?)+\b\S*[A-Z]{2,}\S*)",
    "NUMEROS DE DOCUMENTO": r"doc.\s?SEI n.\s?\d{6,}",
    "NUMEROS DO SEI": r"SEI n.\s?\d{10}",
    "DOTACAO ORCAMENTARIA": r"dotação orçamentária n.\s?\d{23}",
    "ENDEREÇOS": r"Rua\s[\w\s,]+",
    "NOMES DE PESSOAS": r"Sr.\s[\w\s]+|\bFULANA"
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


        print("Texto extraído do PDF:", text)

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

        #removi o misc e mudei a ordem das chaves q aparecem no result
        for key in list(extracted_data.keys()):
            if key not in ["DATAS", "VALOR", "CNPJ", "DOCUMENTOS", "TELEFONES", "EMAIL", "NUMEROS DE CONTRATO", "NOMES DE EMPRESA", "LOCALIZAÇÃO", "NOMES DE PESSOAS", "NOMES DE ORGANIZAÇÕES", "NÚMEROS DE DOCUMENTO", "NÚMEROS DO SEI", "DOTACÃO ORÇAMENTARIA"]:
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
