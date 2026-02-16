import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

def list_models():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY not found in .env")
        return

    try:
        client = genai.Client(api_key=api_key)
        print("Listing available models:")
        models = client.models.list()
        for model in models:
            print(f"- {model.name}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_models()
