import requests
import os

# אנחנו משתמשים בשם המדויק שהגדרת ב-Settings
api_key = os.getenv('RAPIDAPI_KEY')

def check_now():
    if not api_key:
        print("❌ ERROR: GitHub can't find the Secret 'RAPIDAPI_KEY'")
        return

    url = "https://api-football-v1.p.rapidapi.com/v3/timezone" # בדיקה פשוטה בלי ליגות
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    print(f"Testing with key starting with: {api_key[:4]}...")
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ התחברנו! המפתח תקין לחלוטין.")
        else:
            print(f"❌ שגיאת API: {response.json().get('message')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_now()
