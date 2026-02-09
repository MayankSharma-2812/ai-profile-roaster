import openai
import os
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI()

try:
    models = client.models.list()
    print('API connection successful')
except Exception as e:
    print(f'API error: {e}')
