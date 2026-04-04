import requests
import os

api_key = os.getenv('RAPIDAPI_KEY')

def get_kushfc_updates():
    if not api_key:
        print("❌ Secret missing in GitHub!")
        return

    # ליגה 10 = משחקי ידידות ומוקדמות בינלאומיים (מה שביקשת)
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"league": "10", "season": "2025", "last": "10"}
    
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    print("--- KushFC: Fetching International Matches ---")
    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()
            matches = data.get('response', [])
            if matches:
                print(f"✅ הצלחנו! הנה התוצאות האחרונות:")
                for m in matches:
                    home = m['teams']['home']['name']
                    away = m['teams']['away']['name']
                    score = f"{m['goals']['home']}-{m['goals']['away']}"
                    print(f"⚽ {home} {score} {away}")
            else:
                print("⚠️ מחובר, אבל אין משחקים רשומים כרגע בליגה 10.")
        else:
            print(f"❌ שגיאת API מצד GitHub: {response.status_code}")
            print(f"הודעה: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_kushfc_updates()
