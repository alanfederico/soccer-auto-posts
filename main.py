import requests
import os

api_key = os.getenv('RAPIDAPI_KEY')
HOST = "v3.football.api-sports.io"

def final_test():
    if not api_key:
        print("❌ Secret missing!")
        return

    url = f"https://{HOST}/v3/fixtures"
    
    # הבקשה הכי פשוטה שיש: 10 המשחקים האחרונים שהסתיימו
    querystring = {"last": "10"}
    
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": HOST
    }

    print(f"--- KushFC: Fetching last 10 global results ---")
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()
            matches = data.get('response', [])
            
            if matches:
                print(f"✅ הצלחנו! הנה המשחקים האחרונים בעולם:")
                for m in matches:
                    league = m['league']['name']
                    home = m['teams']['home']['name']
                    away = m['teams']['away']['name']
                    score = f"{m['goals']['home']}-{m['goals']['away']}"
                    print(f"⚽ [{league}] {home} {score} {away}")
            else:
                print("⚠️ ה-API מחובר (200 OK) אבל חזר ריק. בודק משחקים חיים...")
                res_live = requests.get(url, headers=headers, params={"live": "all"})
                live_data = res_live.json().get('response', [])
                for m in live_data:
                    print(f"🔥 LIVE: {m['teams']['home']['name']} vs {m['teams']['away']['name']}")
        else:
            print(f"❌ שגיאה: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    final_test()
