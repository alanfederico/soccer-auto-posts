import requests
import os

# משיכת המפתח מה-Secret שהגדרת
api_key = os.getenv('FOOTBALL_API_KEY')
BASE_URL = "https://api.football-data.org/v4/matches"

def fetch_kush_results():
    if not api_key:
        print("❌ Error: FOOTBALL_API_KEY is not set in GitHub Secrets!")
        return

    headers = {'X-Auth-Token': api_key}
    
    # הגדרת התאריך ל-3 באפריל 2026 (המשחק שחיפשת)
    params = {
        "dateFrom": "2026-04-03",
        "dateTo": "2026-04-03"
    }

    print(f"--- KushFC: Fetching Results for 2026-04-03 ---")
    
    try:
        response = requests.get(BASE_URL, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            matches = data.get('matches', [])
            
            if matches:
                print(f"✅ Found {len(matches)} matches!")
                for m in matches:
                    league = m['competition']['name']
                    home = m['homeTeam']['name']
                    away = m['awayTeam']['name']
                    # תוצאה סופית
                    score_h = m['score']['fullTime']['home']
                    score_a = m['score']['fullTime']['away']
                    
                    print(f"⚽ [{league}] {home} {score_h}-{score_a} {away}")
            else:
                print("⚠️ No matches found for this specific date.")
        else:
            print(f"❌ API Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Technical issues: {e}")

if __name__ == "__main__":
    fetch_kush_results()
