import requests
import os

api_key = os.getenv('RAPIDAPI_KEY')
HOST = "v3.football.api-sports.io"

def find_my_matches():
    if not api_key:
        print("❌ Secret missing!")
        return

    url = f"https://{HOST}/v3/fixtures"
    
    # נבדוק את יום שלישי האחרון - זה יביא את כל המשחקים שהיו בעולם באותו יום
    # אם היו מוקדמות מונדיאל, הם חייבים להופיע כאן
    querystring = {"date": "2026-03-31"}
    
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": HOST
    }

    print(f"--- KushFC: Fetching ALL matches from 2026-03-31 ---")
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()
            matches = data.get('response', [])
            
            if matches:
                print(f"✅ הצלחנו! נמצאו {len(matches)} משחקים בתאריך הזה.")
                print("הנה המשחקים המרכזיים שמצאתי:")
                for m in matches:
                    league_name = m['league']['name']
                    home = m['teams']['home']['name']
                    away = m['teams']['away']['name']
                    score = f"{m['goals']['home']}-{m['goals']['away']}"
                    
                    # נדפיס הכל כדי שנוכל לראות את השם המדויק של הליגה
                    print(f"🏆 [{league_name} | ID: {m['league']['id']}] {home} {score} {away}")
            else:
                print("⚠️ התאריך חזר ריק. בוא ננסה אתמול (2026-04-02):")
                querystring["date"] = "2026-04-02"
                response = requests.get(url, headers=headers, params=querystring)
                # ... (בדיקה חוזרת)
        else:
            print(f"❌ שגיאה: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_my_matches()
