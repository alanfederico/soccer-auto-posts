import requests
import os

# הקוד מושך את המפתח מה-Secret ב-GitHub
api_key = os.getenv('RAPIDAPI_KEY')

def test_new_key():
    if not api_key:
        print("❌ ERROR: GitHub still can't find the Secret 'RAPIDAPI_KEY'")
        return

    # בדיקת ליגות - Endpoint בסיסי שכלול בחבילה החינמית
    url = "https://api-football-v1.p.rapidapi.com/v3/leagues"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    print(f"--- Testing New API Key (Starts with: {api_key[:5]}...) ---")
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ YES! המפתח החדש עובד. החיבור תקין לחלוטין.")
            data = response.json()
            if data.get('response'):
                print(f"API is alive. Found {len(data['response'])} leagues.")
        elif response.status_code == 403:
            print("❌ עדיין 403: המפתח מזוהה אבל אין לו הרשאה. וודא שלחצת Subscribe ב-RapidAPI.")
        else:
            print(f"❌ שגיאה אחרת: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_new_key()
