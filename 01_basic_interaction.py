import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables (GEMINI_API_KEY)
load_dotenv()

# Initialize Gemini Client
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ Error: GEMINI_API_KEY not found in .env file.")
    exit(1)

client = genai.Client(api_key=api_key)
MODEL_ID = "gemini-flash-latest"

def get_response(user_input):
    """
    Sends the user input to Gemini and returns the text response.
    """
    print(f"\nSending request to Gemini ({MODEL_ID})...")

    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=user_input,
            config=types.GenerateContentConfig(
                system_instruction="You are a helpful AI assistant explaining concepts simply."
            )
        )
        return response.text
    except Exception as e:
        return f"Error from Gemini: {str(e)}"

def main():
    print("--- 01 Basic Gemini Interaction ---")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        
        reply = get_response(user_input)
        print(f"AI: {reply}\n")

if __name__ == "__main__":
    main()
