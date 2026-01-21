"""Debug script to test API directly"""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
print(f"API Key loaded: {api_key[:20]}..." if api_key else "No API key found")

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "Bibliometric Analysis System"
    }
)

try:
    print("\nTesting API call...")
    response = client.chat.completions.create(
        model="openai/gpt-4o",
        messages=[
            {
                "role": "user",
                "content": "Return only this JSON: [{\"code\": 1702, \"percentage\": 50}, {\"code\": 1705, \"percentage\": 50}]"
            }
        ],
        temperature=0.2,
        max_tokens=100
    )
    
    print(f"\nSuccess! Response:")
    print(response.choices[0].message.content)
    
except Exception as e:
    print(f"\n❌ Error: {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
