import requests

url = "http://127.0.0.1:5001/chat"
dados = {"message": "Olá, chatbot!"}

resposta = requests.post(url, json=dados)

print("Status Code:", resposta.status_code)  # Código de status HTTP
print("Raw Response:", resposta.text)  # Resposta como texto
