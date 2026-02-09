import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

print(f"Testing Groq API key: {groq_api_key[:20]}...")

try:
    client = Groq(api_key=groq_api_key)
    
    # Test with a simple completion
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": "Say 'Hello from Groq!'"}],
        max_tokens=10
    )
    
    print("✅ Groq API working!")
    print(f"Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ Groq API error: {e}")
    print(f"API key length: {len(groq_api_key) if groq_api_key else 0}")
    
    # Try to list models to see if key is valid
    try:
        models = client.models.list()
        print(f"✅ Can list models: {len(list(models))} available")
    except Exception as e2:
        print(f"❌ Cannot list models: {e2}")
