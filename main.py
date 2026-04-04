import requests
import os
from datetime import datetime

api_key = os.getenv('RAPIDAPI_KEY')
HOST = "v3.football.api-sports.io"

def fetch_world_cup_qualifiers():
    if not api_key:
        print("❌ Secret missing!")
        return

    url = f"https://{HOST}/v3/fixtures"
    
    # נחפש משחקים מתאריך 2026-03-31 (יום שלישי האחרון)
    # זה יביא לנו את כל המשחקים שהיו באותו יום בעולם
    querystring = {"date": "2026-03-31"} 
    
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": HOST
    }

    print(f"--- KushFC: Searching for matches on 2026-03-31 ---")
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()
            matches = data.get('response', [])
            
            if matches:
                found_count = 0
                print(f"✅ נמצאו {len(matches)} משחקים בתאריך הזה. הנה המרכזיים:")
                
                for m in matches:
                    league_name = m['league']['name']
                    # נפלטר רק משחקים של נבחרות או ליגות בכירות כדי לא להעמיס
                    if "World Cup" in league_name or "Euro" in league_name or m['league']['id'] == 10:
                        home = m['teams']['home']['name']
                        away = m['teams']['away']['name']
                        score = f"{m['goals']['home']}-{m['goals']['away']}"
                        print(f"🏆 [{league_name}] {home} {score} {away}")
                        found_count += 1
                
                if found_count == 0:
                    print("⚠️ נמצאו משחקים, אבל לא של מוקדמות המונדיאל. הנה דוגמה למה שכן נמצא:")
                    example = matches[0]
                    print(f"⚽ {example['teams']['home']['name']} נגד {example['teams']['away']['name']} ({example['league']['name']})")
            else:
                print("❌ לא נמצאו משחקים בכלל בתאריך 2026-03-31.")
        else:
            print(f"❌ שגיאה: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_world_cup_qualifiers()
