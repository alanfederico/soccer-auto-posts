import requests
import os

api_key = os.getenv('RAPIDAPI_KEY')
HOST = "v3.football.api-sports.io"

def get_anything_available():
    if not api_key:
        print("❌ Secret missing!")
        return

    url = f"https://{HOST}/v3/fixtures"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": HOST
    }

    print(f"--- KushFC: Fetching ANY available matches ---")
    
    try:
        # נסיון 1: משחקים חיים (מכל ליגה שהיא)
        response = requests.get(url, headers=headers, params={"live": "all"})
        matches = response.json().get('response', [])
        
        if not matches:
            # נסיון 2: אם אין חי, נביא את ה-10 האחרונים שהסתיימו בעולם (מכל ליגה)
            print("⚠️ אין משחקים חיים, מנסה תוצאות אחרונות...")
            response = requests.get(url, headers=headers, params={"last": "10"})
            matches = response.json().get('response', [])

        if matches:
            print(f"✅ הצלחנו! נמצאו {len(matches)} משחקים שזמינים במנוי שלך:")
            for m in matches:
                league = m['league']['name']
                home = m['teams']['home']['name']
                away = m['teams']['away']['name']
                score = f"{m['goals']['home']}-{m['goals']['away']}"
                print(f"⚽ [{league}] {home} {score} {away}")
        else:
            print("❌ גם החיפוש הכללי חזר ריק. כדאי לבדוק ב-RapidAPI Dashboard אם המנוי פעיל.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_anything_available()
