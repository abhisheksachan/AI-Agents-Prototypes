import os
import sys
from dotenv import load_dotenv

def check_setup():
    print("--- Environment Verification ---")
    
    # Check Python version
    print(f"Python: {sys.version.split()[0]}")
    
    # Check imports
    missing = []
    try:
        import openai
        print("✅ openai installed")
    except ImportError:
        missing.append("openai")
        print("❌ openai missing")
        
    try:
        import anthropic
        print("✅ anthropic installed")
    except ImportError:
        missing.append("anthropic")
        print("❌ anthropic missing")
        
    try:
        import mcp
        print("✅ mcp installed")
    except ImportError:
        missing.append("mcp")
        print("❌ mcp missing")
        
    if missing:
        print(f"\n⚠️  Please run: pip install {' '.join(missing)}")
    else:
        print("\nAll libraries installed!")

    # Check .env
    load_dotenv()
    key_found = False
    if os.getenv("OPENAI_API_KEY") and not os.getenv("OPENAI_API_KEY").startswith("sk-proj-..."):
        print("✅ OPENAI_API_KEY found")
        key_found = True
    elif os.getenv("ANTHROPIC_API_KEY"):
        print("✅ ANTHROPIC_API_KEY found")
        key_found = True
    else:
        print("❌ No valid API key found in .env (or .env missing)")
        print("   Create a .env file with your API key.")
    
    if key_found and not missing:
        print("\n🚀 You are ready to run the prototypes!")

if __name__ == "__main__":
    check_setup()
