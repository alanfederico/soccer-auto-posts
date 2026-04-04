import requests
import os
from datetime import datetime, timedelta

api_key = os.getenv('RAPIDAPI_KEY')
HOST = "v3.football.api-sports.io"

def get_recent_laliga():
    if not api_key:
        print("❌ Secret missing!")
        return

    url = f"https://{HOST}/v3/fixtures"
    
    # נבדוק את המשחקים של אתמול, היום ומחר כדי לא לפספס בגלל שעות
    today_dt = datetime.now()
    dates_to_check = [
        (today_dt - timedelta(days=1)).strftime('%Y-%m-%d'),
        today_dt.strftime('%Y-%m-%d')
    ]
    
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": HOST
    }

    print(f"--- KushFC: Fetching La Liga (League 140) for dates: {dates_to_check} ---")
    
    found_any = False
    for date in dates_to_check:
        querystring = {"league": "140", "season": "2025", "date": date}
        try:
            response = requests.get(url, headers=headers, params=querystring)
            if response.status_code == 200:
                matches = response.json().get('response', [])
                if matches:
                    print(f"✅ נמצאו משחקים לתאריך {date}:")
                    for m in matches:
                        home = m['teams']['home']['name']
                        away = m['teams']['away']['name']
                        score = f"{m['goals']['home']}-{m['goals']['away']}"
                        print(f"🏟️ {home} {score} {away}")
                    found_any = True
        except Exception as e:
            print(f"Error on {date}: {e}")

    if not found_any:
        print("⚠️ עדיין לא נמצאו משחקים בספרד. מביא את 5 המשחקים האחרונים שהסתיימו בעולם:")
        res = requests.get(url, headers=headers, params={"last": "5"})
        for m in res.json().get('response', []):
            print(f"⚽ [{m['league']['name']}] {m['teams']['home']['name']} {m['goals']['home']}-{m['goals']['away']} {m['teams']['away']['name']}")

if __name__ == "__main__":
    get_recent_laliga()
