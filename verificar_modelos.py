import openai
import os
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

# Configura a API key
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Lista os modelos disponíveis na sua conta
models = client.models.list()

# Exibe os nomes dos modelos disponíveis
for model in models.data:
    print(model.id)
