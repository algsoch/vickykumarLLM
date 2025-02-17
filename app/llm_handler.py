# openai.api_key = 
import openai
import os

AIPROXY_TOKEN = os.getenv("eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjI0ZjIwMDY0MzhAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.cVZQ9PdwcVpCw0uUIchzua3Skut2HmVioyiE47VkDkU")
openai.api_key = AIPROXY_TOKEN

def extract_email_with_llm():
    """Extracts email sender from /data/email.txt using LLM"""
    file_path = "data/email.txt"
    if not os.path.exists(file_path):
        raise FileNotFoundError("email.txt not found")

    with open(file_path, "r") as file:
        email_content = file.read()

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "Extract the sender's email address."},
                  {"role": "user", "content": email_content}]
    )
    return response["choices"][0]["message"]["content"]

def extract_credit_card_with_llm():
    """Extracts credit card number from /data/credit-card.png using OCR+LLM"""
    file_path = "data/credit-card.png"
    if not os.path.exists(file_path):
        raise FileNotFoundError("credit-card.png not found")

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "Extract the credit card number from this image."},
                  {"role": "user", "content": f"Image file: {file_path}"}]
    )
    return response["choices"][0]["message"]["content"]
