from flask import Flask, render_template, request, redirect, url_for, session
from flask_bootstrap import Bootstrap
import spacy
import fitz  

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessário para usar sessões
Bootstrap(app)

nlp = spacy.load("pt_core_news_sm")

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

        # Print para verificar se o texto está sendo extraído corretamente
        print("Texto extraído do PDF:", text)

        doc = nlp(text)

        # Lógica para extração de informações
        cnpjs = []
        valores = []

        #Nomeação das entidades
        for entidade in doc.ents:
            print(f"Entidade detectada: {entidade.text} - Label: {entidade.label_}")
            if entidade.label_ == "CNPJ":
                cnpjs.append(entidade.text)
            elif entidade.label_ == "VALOR":
                valores.append(entidade.text)

        # Exemplo de dados processados
        processed_data = {
            "filename": filename,
            "cnpjs": cnpjs,
            "valores": valores
        }

        # Print para verificar os dados processados
        print("Dados processados:", processed_data)

        # Armazenar os dados na sessão
        session['processed_data'] = processed_data

        return redirect(url_for('result'))

@app.route('/result')
def result():
    result = session.get('processed_data', {})
    print("Dados recuperados da sessão:", result)
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
