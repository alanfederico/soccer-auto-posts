import requests
import os
import json

# וודא שה-Secret ב-GitHub נקרא בדיוק RAPID_API_KEY
RAPID_API_KEY = os.getenv('RAPID_API_KEY')

def final_debug():
    # בקשה ל-10 משחקים מכל מקום בעולם שהסתיימו הרגע
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"last": "10"}
    
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    print(f"--- Debugging Connection ---")
    print(f"Key exists in environment: {bool(RAPID_API_KEY)}")
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        
        if 'response' in data and len(data['response']) > 0:
            print("--- Success! Found matches: ---")
            for match in data['response']:
                league = match['league']['name']
                home = match['teams']['home']['name']
                away = match['teams']['away']['name']
                print(f"[{league}] {home} vs {away}")
        else:
            print("--- Still Empty ---")
            print("API Message:", data.get('message', 'No message'))
            print("Errors:", data.get('errors', []))
            
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    final_debug()
