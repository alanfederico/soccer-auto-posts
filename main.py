import requests
import os

# שימוש בשם ה-Secret המדויק מהפרויקט הראשי שלך
api_key = os.getenv('FOOTBALL_API_KEY')
BASE_URL = "https://api.football-data.org/v4/matches"

def check_results():
    if not api_key:
        print("❌ שגיאה: ה-Secret שנקרא FOOTBALL_API_KEY לא נמצא!")
        return

    headers = {'X-Auth-Token': api_key}
    
    # בדיקת המשחקים של אתמול (היום שבו היה המשחק שראית)
    # 2026-04-03
    params = {
        "dateFrom": "2026-04-03",
        "dateTo": "2026-04-03"
    }

    print(f"--- KushFC: Checking Football-Data.org for April 3rd ---")
    
    try:
        response = requests.get(BASE_URL, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            matches = data.get('matches', [])
            
            if matches:
                print(f"✅ נמצאו {len(matches)} משחקים במערכת.")
                for m in matches:
                    league = m['competition']['name']
                    home = m['homeTeam']['name']
                    away = m['awayTeam']['name']
                    score_h = m['score']['fullTime']['home']
                    score_a = m['score']['fullTime']['away']
                    
                    # הדפסה ברורה של התוצאות
                    print(f"⚽ [{league}] {home} {score_h}-{score_a} {away}")
            else:
                print("⚠️ לא נמצאו משחקים רשומים לתאריך הזה.")
        else:
            print(f"❌ שגיאה בחיבור (סטטוס {response.status_code}): {response.text}")
            
    except Exception as e:
        print(f"❌ תקלה בהרצה: {e}")

if __name__ == "__main__":
    check_results()
