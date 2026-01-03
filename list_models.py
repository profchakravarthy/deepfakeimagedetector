import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

GENAI_API_KEY = os.getenv("GENAI_API_KEY")

if not GENAI_API_KEY:
    print("Error: GENAI_API_KEY not found in environment variables.")
else:
    try:
        client = genai.Client(api_key=GENAI_API_KEY)
        # List models and filter for those that likely support content generation
        print("Fetching available models...")
        for model in client.models.list():
            print(f"- {model.name}")
            
    except Exception as e:
        print(f"Error listing models: {e}")
