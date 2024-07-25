# Passos para rodar
___

1 Deletar as pastas Myvenv e Venv

2 Rodar os seguintes comandos:

```shell
python -m venv venv
```
```shell
.\venv\Scripts\activate
```
```shell
pip install -r requirements.txt
```
```shell
python app.py
```

3 Caso não de certo seguir os seguintes passos
```shell
pip install Flask
```
```shell
pip install flask_bootstrap
```
```shell
python -m spacy download pt_core_news_sm
```
```shell
pip install PyMuPDF
```

4 Rode novamente o comando
```shell
python app.py
```

5 Caso a estilização não esteja sendo carregado executar os seguintes comandos:
```shell
npm install -D tailwindcss
```
```shell
npx tailwindcss init
```
```shell
npm run build -css
```
___
