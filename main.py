import requests
import os

RAPID_API_KEY = os.getenv('RAPID_API_KEY')

def test_international_matches():
    # ID 1 הוא בדרך כלל למשחקים בינלאומיים (World)
    # אנחנו נבקש את ה-10 האחרונים שהסתיימו (status = FT)
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"league": "1", "season": "2026", "last": "10"}
    
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    print("--- Fetching Last 10 International Matches ---")
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        
        if 'response' in data and len(data['response']) > 0:
            for match in data['response']:
                league_name = match['league']['name']
                home = match['teams']['home']['name']
                away = match['teams']['away']['name']
                score = f"{match['goals']['home']} - {match['goals']['away']}"
                status = match['fixture']['status']['short']
                print(f"[{league_name}] {home} {score} {away} ({status})")
        else:
            print("No international matches found. Printing full response for debug:")
            print(data)
            
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    test_international_matches()
