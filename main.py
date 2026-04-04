import requests
import os
from datetime import datetime

api_key = os.getenv('RAPIDAPI_KEY')
HOST = "v3.football.api-sports.io"

def check_laliga_today():
    if not api_key:
        print("❌ Secret missing!")
        return

    url = f"https://{HOST}/v3/fixtures"
    
    # תאריך של היום (2026-04-03)
    today = datetime.now().strftime('%Y-%m-%d')
    
    # חיפוש לפי ליגה 140 (ספרד) ותאריך היום
    querystring = {
        "league": "140",
        "season": "2025", # עונת 2025/26
        "date": today
    }
    
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": HOST
    }

    print(f"--- KushFC: Checking La Liga Matches for Today ({today}) ---")
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()
            matches = data.get('response', [])
            
            if matches:
                print(f"✅ נמצאו {len(matches)} משחקים בליגה הספרדית!")
                for m in matches:
                    home = m['teams']['home']['name']
                    away = m['teams']['away']['name']
                    status = m['fixture']['status']['long']
                    score = f"{m['goals']['home']}-{m['goals']['away']}"
                    print(f"🏟️ {home} {score} {away} ({status})")
            else:
                print(f"⚠️ לא נמצאו משחקים של לה-ליגה להיום ({today}).")
                print("מנסה להביא את כל המשחקים מכל הליגות שהיו היום כדי לראות מה פספסנו...")
                
                res_all = requests.get(url, headers=headers, params={"date": today})
                all_matches = res_all.json().get('response', [])
                if all_matches:
                    print(f"נמצאו {len(all_matches)} משחקים בליגות אחרות. הנה דוגמה:")
                    for m in all_matches[:5]:
                        print(f"⚽ [{m['league']['name']}] {m['teams']['home']['name']} vs {m['teams']['away']['name']}")
        else:
            print(f"❌ שגיאה: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_laliga_today()
