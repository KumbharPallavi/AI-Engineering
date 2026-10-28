import os
import requests
from dotenv import load_dotenv

# Load API key from the root or local .env file
load_dotenv(dotenv_path=".env")  # Checks root .env first
load_dotenv()                       # Fallback to local .env

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise ValueError("API key not found. Ensure OPENROUTER_API_KEY is set in your .env file.")

def chat_with_openrouter():
    print("=" * 50)
    print("  OpenRouter Interactive CLI Chat (type 'exit' to quit)")
    print("=" * 50)

    # Maintain conversation memory locally
    messages = [
        {"role": "system", "content": "You are a helpful, concise AI coding partner."}
    ]

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    while True:
        user_input = input("\nYou: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ["exit", "quit"]:
            print("Ending chat. Goodbye!")
            break

        # Append user message to history
        messages.append({"role": "user", "content": user_input})

        payload = {
            "model": "openrouter/free",  # Automatically picks an active free model
            "messages": messages
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            res_data = response.json()

            if "choices" in res_data:
                reply = res_data["choices"][0]["message"]["content"]
                print(f"\nAI: {reply}")
                # Append assistant response to preserve chat context
                messages.append({"role": "assistant", "content": reply})
            else:
                print(f"\nAPI Error: {res_data}")

        except Exception as e:
            print(f"\nRequest failed: {e}")

if __name__ == "__main__":
    chat_with_openrouter()