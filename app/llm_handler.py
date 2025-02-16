import openai
import os

openai.api_key = os.getenv("eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjI0ZjIwMDY0MzhAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.cVZQ9PdwcVpCw0uUIchzua3Skut2HmVioyiE47VkDkU")

def process_task(data):
    """Processes text using GPT."""
    prompt = data.get("prompt", "")
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]
