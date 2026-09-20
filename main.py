import os
import time
import requests
from google import genai

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, data=data)

def check_airdrops():
    prompt = "Find 3 latest active crypto airdrops with high potential in 2026. Provide brief details and links."
    
    # 503 এরর এড়াতে ৩ বার চেষ্টা করবে এবং ব্যাকআপ মডেল ব্যবহার করবে
    models_to_try = ["gemini-3.6-flash", "gemini-2.5-flash"]
    
    for model_name in models_to_try:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                if response.text:
                    send_telegram_message(f"🚀 *New Crypto Airdrop Alert!*\n\n{response.text}")
                    return
            except Exception as e:
                print(f"Attempt {attempt + 1} with {model_name} failed: {e}")
                time.sleep(5)  # ৫ সেকেন্ড অপেক্ষা করে আবার চেষ্টা করবে

def main():
    check_airdrops()

if __name__ == "__main__":
    main()
