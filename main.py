import requests
import os

api_key = os.getenv('RAPIDAPI_KEY')
HOST = "v3.football.api-sports.io"

def scan_recent_matches():
    if not api_key:
        print("❌ Secret missing!")
        return

    url = f"https://{HOST}/v3/fixtures"
    
    # נבקש את ה-50 המשחקים האחרונים שהסתיימו בעולם באופן כללי
    querystring = {"last": "50"}
    
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": HOST
    }

    print(f"--- KushFC: Scanning last 50 matches for World Cup Qualifiers ---")
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()
            matches = data.get('response', [])
            
            if matches:
                print(f"🔎 נסרקו {len(matches)} משחקים. הנה מה שמצאתי:")
                found = False
                for m in matches:
                    league = m['league']['name']
                    league_id = m['league']['id']
                    home = m['teams']['home']['name']
                    away = m['teams']['away']['name']
                    
                    # מחפשים מילות מפתח של מוקדמות או נבחרות
                    if any(word in league for word in ["World Cup", "Qualifiers", "UEFA", "FIFA"]):
                        print(f"✅ מצאתי! [ID: {league_id}] {league}: {home} נגד {away}")
                        found = True
                
                if not found:
                    print("⚠️ לא מצאתי מוקדמות מונדיאל ב-50 המשחקים האחרונים.")
                    print("הנה הליגה של המשחק הכי טרי ברשימה:")
                    print(f"⚽ {matches[0]['league']['name']} (ID: {matches[0]['league']['id']})")
            else:
                print("❌ ה-API חזר ריק. ייתכן שאין משחקים רשומים ב-7 הימים האחרונים.")
        else:
            print(f"❌ שגיאה: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scan_recent_matches()
