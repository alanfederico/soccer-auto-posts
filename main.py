import requests
import os

api_key = os.getenv('RAPIDAPI_KEY')

def get_kushfc_updates():
    if not api_key:
        print("❌ Secret missing in GitHub!")
        return

    # ננסה את ה-Host האלטרנטיבי של ה-API
    # לפעמים זה 'api-football-v1.p.rapidapi.com' 
    # ולפעמים זה 'v3.football.api-sports.io'
    
    hosts = [
        "api-football-v1.p.rapidapi.com",
        "v3.football.api-sports.io"
    ]
    
    for host in hosts:
        print(f"--- Trying with Host: {host} ---")
        
        url = f"https://{host}/v3/fixtures"
        querystring = {"league": "10", "season": "2025", "last": "5"}
        
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": host
        }

        try:
            response = requests.get(url, headers=headers, params=querystring)
            print(f"Status for {host}: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                matches = data.get('response', [])
                if matches:
                    print(f"✅ הצלחנו עם {host}! הנה המשחקים:")
                    for m in matches:
                        home = m['teams']['home']['name']
                        away = m['teams']['away']['name']
                        print(f"⚽ {home} נגד {away}")
                    return # עוצרים כאן כי מצאנו מה עובד
                else:
                    print(f"⚠️ מחובר ל-{host} אבל אין משחקים.")
            else:
                print(f"❌ שגיאה ב-{host}: {response.text}")
                
        except Exception as e:
            print(f"Error with {host}: {e}")

if __name__ == "__main__":
    get_kushfc_updates()
