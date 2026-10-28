import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API key securely
api_key = os.environ.get("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY is not set in the environment or .env file.")

# Initialize the OpenAI client configured for OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# Make a chat completion request
response = client.chat.completions.create(
    model="openai/gpt-4o-mini",  # Changed from anthropic/claude-3.5-sonnet
    messages=[{"role": "user", "content": "Hello, how are you?"}]
)

# Print the response and token usage
print("Response:", response.choices[0].message.content)
print("\n--- Token Usage ---")
print("Prompt tokens:", response.usage.prompt_tokens)
print("Completion tokens:", response.usage.completion_tokens)
print("Total tokens:", response.usage.total_tokens)