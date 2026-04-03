import requests
import os

RAPID_API_KEY = os.getenv('RAPIDAPI_KEY')

# רשימת IDs של הליגות ב-API החדש
LEAGUES_TO_TEST = {
    "Premier League": 39,
    "Champions League": 2,
    "MLS": 253,
    "La Liga": 140
}

def test_full_api():
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    for name, id in LEAGUES_TO_TEST.items():
        print(f"\n--- Testing {name} (ID: {id}) ---")
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        querystring = {"league": str(id), "season": "2024", "last": "3"}

        try:
            response = requests.get(url, headers=headers, params=querystring)
            data = response.json()
            
            if 'response' in data and len(data['response']) > 0:
                for match in data['response']:
                    home = match['teams']['home']['name']
                    away = match['teams']['away']['name']
                    print(f"[OK] {home} vs {away}")
            else:
                print(f"[!] No data or limited access for {name}")
        except Exception as e:
            print(f"[ERROR] {name}: {e}")

if __name__ == "__main__":
    test_full_api()
