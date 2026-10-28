import tiktoken

# Choose the encoding corresponding to your target model family
encoding = tiktoken.encoding_for_model("gpt-4o")

# 1. Text to Tokens (Encode)
text = "Hello, OpenRouter!"
token_ids = encoding.encode(text)
print("Token IDs:", token_ids)

# 2. Tokens to Text (Decode)
decoded_text = encoding.decode(token_ids)
print("Decoded Text:", decoded_text)