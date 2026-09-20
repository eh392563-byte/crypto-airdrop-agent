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

def analyze_opportunity(title, link, description):
    prompt = f"""
    Analyze the following crypto opportunity/airdrop:
    Title: {title}
    URL: {link}
    Description: {description}
    
    Tasks:
    1. Check for scam indicators (phishing URL, unrealistic guarantees, asking for private keys).
    2. Assess legitimacy and effort vs reward.
    3. Output 'LEGIT' or 'SCAM' on the first line.
    4. Provide a 2-sentence summary in Bengali highlighting actions needed.
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    return response.text

def main():
    sample_title = "Example Verified Airdrop Campaign"
    sample_link = "https://example.com/airdrop"
    sample_desc = "Join testnet and receive early ecosystem tokens."
    
    analysis = analyze_opportunity(sample_title, sample_link, sample_desc)
    
    if "LEGIT" in analysis.upper():
        msg = f"🚀 **নতুন ভেরিফাইড এয়ারড্রপ সুযোগ!**\n\n📌 **টাইটেল:** {sample_title}\n🔗 **লিংক:** {sample_link}\n\n🤖 **AI বিশ্লেষণ:**\n{analysis}"
        send_telegram_message(msg)

if __name__ == "__main__":
    main()
