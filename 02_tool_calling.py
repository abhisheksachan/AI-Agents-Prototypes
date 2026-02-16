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

# --- 1. Define Tools (Plain Python Functions) ---

def get_current_weather(location: str, unit: str = "celsius"):
    """
    Get the current weather in a given location.
    
    Args:
        location: The city and state, e.g. San Francisco, CA
        unit: The temperature unit (celsius or fahrenheit)
    """
    print(f"DEBUG [Tool]: get_current_weather('{location}', unit='{unit}')")
    
    # Mock data logic
    loc = location.lower()
    if "london" in loc:
        return "Error: Weather service for London is under maintenance."
    elif "tokyo" in loc:
        return json.dumps({"location": "Tokyo", "temperature": "10", "unit": "celsius"})
    elif "paris" in loc:
        return json.dumps({"location": "Paris", "temperature": "22", "unit": "celsius"})
    else:
        return json.dumps({"location": location, "temperature": "72", "unit": "fahrenheit"})

def calculate(expression: str):
    """
    Evaluate a simple mathematical expression.
    
    Args:
        expression: The math expression to evaluate, e.g. '25 + 15'
    """
    print(f"DEBUG [Tool]: calculate('{expression}')")
    try:
        # In a real app, use a safer parser like 'numexpr' or 'simpleeval'
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

# --- 2. Main execution ---

def run_demo():
    print("--- 02 Gemini Tool Calling Demo ---")
    
    question = "What is the temperature in Paris and Tokyo added together?"
    print(f"Question: {question}")

    # For Gemini, we just pass the function objects themselves!
    tools = [get_current_weather, calculate]

    try:
        # We use automatic_function_calling=True by default in the SDK's high-level API
        # but here we pass it in the config to be explicit.
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=question,
            config=types.GenerateContentConfig(
                tools=tools
            )
        )
        
        # Inspection of the turns
        print("\n--- Execution Steps ---")
        for i, part in enumerate(response.candidates[0].content.parts):
            if part.text:
                print(f"AI Response: {part.text}")
            if part.function_call:
                print(f"AI decided to use tool: {part.function_call.name} with {part.function_call.args}")

        print("\n--- Final Result ---")
        print(response.text)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_demo()
