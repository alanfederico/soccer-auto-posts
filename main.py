import requests
import os
import json

# --- זה הקוד הקצר והחסין שביקשת ---
# הוא בודק גם עם קו תחתון וגם בלי, ככה שלא משנה מה כתבת ב-Settings
RAPID_API_KEY = os.getenv('RAPID_API_KEY') or os.getenv('RAPIDAPI_KEY')

def test_connection():
    if not RAPID_API_KEY:
        print("❌ CRITICAL ERROR: No API Key found in GitHub Secrets!")
        return

    # בדיקת משחקי מוקדמות/ידידות (League 10 או 1)
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"league": "10", "season": "2025", "last": "5"}
    
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    print(f"--- Testing Connection with Key: {RAPID_API_KEY[:5]}*** ---")
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('response'):
                print("✅ SUCCESS! Found matches:")
                for match in data['response']:
                    print(f"- {match['teams']['home']['name']} vs {match['teams']['away']['name']}")
            else:
                print("⚠️ Connected, but no matches found for this league/season.")
        else:
            print(f"❌ API Error: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_connection()
