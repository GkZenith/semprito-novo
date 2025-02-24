import os
import json
import gspread
from flask import Flask, request, jsonify
from google.oauth2.service_account import Credentials
import google.generativeai as genai
from dotenv import load_dotenv
from flask_cors import CORS

# Carrega variáveis do .env
load_dotenv()

# Configuração da API do Gemini
GEMINI_API_KEY = os.getenv("AIzaSyCW2jwBml0cBGIFpAqW5BxKQikU9SKD2G0")
genai.configure(api_key=GEMINI_API_KEY)

# Configuração do Flask
app = Flask(__name__)
CORS(app)

# Configuração do Google Sheets
SERVICE_ACCOUNT_FILE = "seu_arquivo.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# Abra a planilha pelo ID
SHEET_ID = "1Eywp3oueYk9BJY2wfRE-vuroElBH5KoTcyKHEI1w9xY"
sheet = client.open_by_key(SHEET_ID).sheet1

# Rota principal
@app.route("/")
def home():
    return "Servidor do chatbot está rodando! Use a rota /chat para enviar mensagens."

# Função para buscar dados na planilha
def buscar_dados(termo_pesquisa):
    registros = sheet.get_all_records()
    for registro in registros:
        if str(registro["RA"]) == str(termo_pesquisa) or termo_pesquisa.lower() in registro["Nome"].lower():
            return registro
    return None

# Função para processar perguntas sobre ASO e férias
def processar_pergunta(pergunta):
    palavras = pergunta.split()
    for palavra in palavras:
        if palavra.isdigit():
            dados = buscar_dados(palavra)
            if dados:
                resposta = f"Nome: {dados['Nome']}\n"
                if "aso" in pergunta:
                    resposta += f"Vencimento do ASO: {dados['Dia de encerramento ASO']}\n"
                    resposta += f"Faltam {dados['Quantos dias faltam para vencer ASO']} dias."
                if "férias" in pergunta:
                    resposta += f"Início das férias: {dados['Dia de início das férias']}\n"
                    resposta += f"Término das férias: {dados['Dia fim das férias']}\n"
                    resposta += f"Faltam {dados['Quantos dias faltam para tirar as férias']} dias."
                return resposta
    return None

# Rota do chatbot
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "").lower().strip()

    if not user_message:
        return jsonify({"error": "Mensagem não fornecida"}), 400

    # Primeiro tenta buscar dados na planilha
    resposta = processar_pergunta(user_message)
    if resposta:
        return jsonify({"reply": resposta})

    # Se não encontrar na planilha, usa o Gemini
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(user_message)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para testar a leitura dos dados da planilha
@app.route("/dados", methods=["GET"])
def obter_dados():
    try:
        registros = sheet.get_all_records()
        return jsonify(registros)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
