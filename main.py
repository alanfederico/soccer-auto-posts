import requests
import os

api_key = os.getenv('RAPIDAPI_KEY')
# ה-Host שעבד לנו ב-200 OK
HOST = "v3.football.api-sports.io"

def get_world_cup_results():
    if not api_key:
        print("❌ Secret missing!")
        return

    url = f"https://{HOST}/v3/fixtures"
    
    # הגדרות ספציפיות למוקדמות מונדיאל אירופה
    querystring = {
        "league": "10", 
        "season": "2026", # העונה הנוכחית של המוקדמות
        "last": "20"      # ה-20 האחרונים כדי לוודא שנתפוס את יום שלישי
    }
    
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": HOST
    }

    print(f"--- KushFC: Fetching World Cup Qualifiers (League 10) ---")
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()
            matches = data.get('response', [])
            
            if matches:
                print(f"✅ הצלחנו! נמצאו {len(matches)} משחקים:")
                for m in matches:
                    home = m['teams']['home']['name']
                    away = m['teams']['away']['name']
                    score = f"{m['goals']['home']}-{m['goals']['away']}"
                    date = m['fixture']['date'][:10] # לוקח רק את התאריך
                    print(f"📅 {date} | ⚽ {home} {score} {away}")
            else:
                print("⚠️ לא נמצאו משחקים. מנסה עונה 2025 ליתר ביטחון...")
                querystring["season"] = "2025"
                response = requests.get(url, headers=headers, params=querystring)
                matches = response.json().get('response', [])
                for m in matches:
                    print(f"⚽ {m['teams']['home']['name']} {m['goals']['home']}-{m['goals']['away']} {m['teams']['away']['name']}")
        else:
            print(f"❌ שגיאה: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_world_cup_results()
