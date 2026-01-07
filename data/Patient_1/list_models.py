from google import genai

API_KEY = "AIzaSyDatDvj9ZPKwMUVZnCIFO0dorxGiI53oB8"
client = genai.Client(api_key=API_KEY)

print("🔍 Checking available models for your API key...")

try:
    # List all models that support generating content
    for m in client.models.list():
        if "generateContent" in m.supported_actions:
            print(f"✅ Available: {m.name}")
except Exception as e:
    print(f"❌ Could not list models: {e}")