import requests
import os

# הקוד יבדוק את כל השמות האפשריים שהזכרנו כדי למצוא את המפתח
api_key = (os.getenv('RAPIDAPI_KEY') or 
           os.getenv('Football_result') or 
           os.getenv('Footbal_resulst'))

def run_test():
    if not api_key:
        print("❌ ERROR: GitHub still can't find the Secret!")
        print("Check your Settings -> Secrets -> Actions again.")
        return

    # בדיקת חיבור בסיסית
    url = "https://api-football-v1.p.rapidapi.com/v3/timezone"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    print(f"--- Testing Connection ---")
    try:
        response = requests.get(url, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ הצלחנו! המפתח זוהה והחיבור תקין.")
        else:
            print(f"❌ שגיאת API: {response.json().get('message')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_test()
