import requests
import os

api_key = os.getenv('RAPIDAPI_KEY')
HOST = "v3.football.api-sports.io"

def rescue_mission():
    if not api_key:
        print("❌ Secret missing!")
        return

    # שלב 1: בדיקה אילו ליגות בכלל פתוחות לך בחשבון
    url_leagues = f"https://{HOST}/v3/leagues"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": HOST
    }

    print(f"--- KushFC: Checking available leagues ---")
    
    try:
        # ננסה לבדוק רק אם הליגה הספרדית (140) או אנגליה (39) זמינות
        response = requests.get(url_leagues, headers=headers, params={"id": "140"})
        if response.status_code == 200:
            leagues = response.json().get('response', [])
            if leagues:
                print(f"✅ ליגה ספרדית זמינה! מנסה לשלוף משחקים חיים מכל העולם...")
                
                # אם הליגות זמינות, ננסה לשלוף את כל המשחקים של היום ללא סינון ליגה
                url_fixtures = f"https://{HOST}/v3/fixtures"
                # נשתמש בפרמטר 'live' כדי לראות אם משהו רץ עכשיו, זה הכי אמין
                res_live = requests.get(url_fixtures, headers=headers, params={"live": "all"})
                matches = res_live.json().get('response', [])
                
                if matches:
                    for m in matches[:10]:
                        print(f"🔥 LIVE: {m['teams']['home']['name']} {m['goals']['home']}-{m['goals']['away']} {m['teams']['away']['name']}")
                else:
                    print("⚠️ אין משחקים חיים. מנסה לשלוף את המשחקים של אתמול (2026-04-02)...")
                    res_yesterday = requests.get(url_fixtures, headers=headers, params={"date": "2026-04-02"})
                    y_matches = res_yesterday.json().get('response', [])
                    for m in y_matches[:10]:
                        print(f"🏟️ {m['teams']['home']['name']} {m['goals']['home']}-{m['goals']['away']} {m['teams']['away']['name']} ({m['league']['name']})")
            else:
                print("❌ הליגה הספרדית לא מופיעה במנוי שלך.")
        else:
            print(f"❌ שגיאת חיבור: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    rescue_mission()
