import os
import requests
from bs4 import BeautifulSoup
from google import genai

# Environment Variables
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Initialize Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, data=data)

def check_airdrops():
    # Example logic for checking airdrops
    prompt = "Find 3 latest active crypto airdrops with high potential in 2026. Provide brief details and links."
    
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    
    if response.text:
        send_telegram_message(f"🚀 *New Crypto Airdrop Alert!*\n\n{response.text}")

def main():
    check_airdrops()

if __name__ == "__main__":
    main()
