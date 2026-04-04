import requests
import os

api_key = os.getenv('RAPIDAPI_KEY')
HOST = "v3.football.api-sports.io"

def get_available_data():
    if not api_key:
        print("❌ Secret missing in GitHub!")
        return

    url = f"https://{HOST}/v3/fixtures"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": HOST
    }

    print(f"--- KushFC: Searching for ANY available matches ---")
    
    try:
        # נסיון 1: משחקים חיים מכל העולם
        response = requests.get(url, headers=headers, params={"live": "all"})
        matches = response.json().get('response', [])
        
        if not matches:
            # נסיון 2: 15 התוצאות האחרונות שהסתיימו (מכל הליגות)
            print("⚠️ אין משחקים חיים, בודק תוצאות אחרונות...")
            response = requests.get(url, headers=headers, params={"last": "15"})
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
            print("❌ גם החיפוש הכללי חזר ריק. ייתכן שיש בעיה זמנית ב-RapidAPI.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_available_data()
