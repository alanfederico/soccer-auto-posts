import requests
import os

# עדכון לשם המדויק שנתת ב-GitHub Secrets
api_key = os.getenv('Football_result')

def run_update():
    if not api_key:
        print("❌ ERROR: GitHub can't find the Secret 'Football_result'")
        print("וודא שהשם ב-Settings הוא בדיוק Football_result")
        return

    # ליגה 10 = משחקי ידידות ומוקדמות מונדיאל/יורו
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"league": "10", "season": "2025", "last": "10"}
    
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    print(f"--- בודק משחקים בינלאומיים עבור KushFC ---")
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            matches = data.get('response', [])
            if matches:
                print(f"✅ הצלחנו! נמצאו {len(matches)} משחקים:")
                for m in matches:
                    home = m['teams']['home']['name']
                    away = m['teams']['away']['name']
                    res = f"{m['goals']['home']}-{m['goals']['away']}"
                    print(f"⚽ {home} {res} {away}")
            else:
                print("⚠️ החיבור הצליח, אבל אין משחקים פעילים בליגה 10 כרגע.")
        else:
            print(f"❌ שגיאת API: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_update()
