import openai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

print(f"Testing API key: {api_key[:20]}...")

client = openai.OpenAI(api_key=api_key)

try:
    # Try to get account info
    usage = client.usage.retrieve()
    print("✅ API key is valid!")
    print(f"Current usage: {usage}")
except Exception as e:
    print(f"❌ API key error: {e}")
    
    # Try a simpler test - list models
    try:
        models = client.models.list()
        print("✅ API key can list models - key is valid")
        print(f"Available models: {len(list(models))}")
    except Exception as e2:
        print(f"❌ Even model listing failed: {e2}")
