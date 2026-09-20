import os
import time
from google import genai
import requests

# গিটহাব সিক্রেটস থেকে ক্রেডেনশিয়ালস লোড করা হচ্ছে
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Gemini ক্লাইন্ট ইনিশিয়ালাইজ করা
client = genai.Client(api_key=GEMINI_API_KEY)

def send_telegram_message(message):
    """টেলিগ্রাম বোটে মেসেজ পাঠানোর ফাংশন"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    
    # ৫টি ট্রাই করার অপশন (503 বা নেটওয়ার্ক এরর এড়াতে)
    for attempt in range(5):
        try:
            response = requests.post(url, json=payload, timeout=10)
            result = response.json()
            if result.get("ok"):
                print("টেলিগ্রামে সফলভাবে মেসেজ পাঠানো হয়েছে!")
                return True
            else:
                print(f"Telegram API Response Error: {result}")
        except Exception as e:
            print(f"Attempt {attempt + 1} failed to send message: {e}")
        
        time.sleep(5)
    return False

def check_airdrops():
    """জেমিনি এআই ব্যবহার করে এয়ারড্রপ সার্চ এবং বাংলায় ক্লেইম গাইড ফরম্যাট করার ফাংশন"""
    prompt = (
        "Find 3 latest active crypto airdrops with high potential in 2026. "
        "Provide all details, direct links, and clear step-by-step instructions on "
        "how to claim them. Write the entire response in clear Bengali (বাংলা)."
    )
    
    models_to_try = ["gemini-2.5-flash", "gemini-2.5-pro"]
    
    for model_name in models_to_try:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                if response and response.text:
                    final_message = f"🚀 নতুন ক্রিপ্টো এয়ারড্রপ অ্যালার্ট!\n\n{response.text}"
                    send_telegram_message(final_message)
                    return
            except Exception as e:
                print(f"Attempt {attempt + 1} with {model_name} failed: {e}")
                time.sleep(5)
                
    print("দুঃখিত, সব মডেল চেষ্টা করার পরও জেমিনি থেকে তথ্য আনা সম্ভব হয়নি।")

if __name__ == "__main__":
    check_airdrops()
