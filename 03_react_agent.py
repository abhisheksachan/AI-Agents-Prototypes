import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# Initialize Gemini Client
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ Error: GEMINI_API_KEY not found in .env file.")
    exit(1)

client = genai.Client(api_key=api_key)
MODEL_ID = "gemini-flash-latest"

# --- Tools ---

def get_weather(location: str):
    """Get the weather for a location."""
    print(f"DEBUG [Agent Action]: get_weather('{location}')")
    if "london" in location.lower():
        return "15°C, rainy"
    elif "paris" in location.lower():
        return "20°C, sunny"
    else:
        return "25°C, clear skies"

def calculate(expression: str):
    """Evaluate a mathematical expression expression."""
    print(f"DEBUG [Agent Action]: calculate('{expression}')")
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

class GeminiAgent:
    def __init__(self):
        self.tools = [get_weather, calculate]
        
    def ask(self, user_input):
        print(f"\nUser: {user_input}")
        
        # Gemini 'chats' automatically manage history and tool loops
        chat_session = client.chats.create(
            model=MODEL_ID,
            config=types.GenerateContentConfig(
                tools=self.tools,
                system_instruction="You are a helpful ReAct agent. Solve the user's request. If multiple tools are needed, use them sequentially."
            )
        )
        
        print("--- Agent is thinking/acting ---")
        response = chat_session.send_message(user_input)
        
        print(f"\nFinal Answer: {response.text}")

if __name__ == "__main__":
    agent = GeminiAgent()
    
    # This query forces the agent to use weather twice and math once
    agent.ask("What is the weather in London and Paris? Then add the temperatures together.")
