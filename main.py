import requests
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

# הגדרות RapidAPI
API_KEY = os.getenv('FOOTBALL_API_KEY')
API_HOST = "api-football-v1.p.rapidapi.com" # וודא שזה ה-host שרשום לך ב-RapidAPI

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

# נבקש משחקים מהתאריך של היום
today = datetime.now().strftime('%Y-%m-%d')
querystring = {"date": today, "status": "FT"} # FT = Finished (משחקים שהסתיימו)

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST
}

def create_post():
    print(f"Checking matches for date: {today}...")
    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()

        if not data.get('response'):
            print("No finished matches found for today yet.")
            return

        # לוקחים את המשחק הראשון שמצאנו שנגמר
        match = data['response'][0]
        home = match['teams']['home']['name']
        away = match['teams']['away']['name']
        score_home = match['goals']['home']
        score_away = match['goals']['away']
        league_name = match['league']['name']

        text_to_print = f"{league_name}: {home} {score_home} - {score_away} {away}"
        print(f"Found: {text_to_print}")

        # יצירת התמונה
        if not os.path.exists("background.jpg"):
            print("Error: background.jpg missing!")
            return

        img = Image.open("background.jpg")
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        
        # כתיבת הטקסט (מיקום 100, 200 - תשנה לפי הצורך)
        draw.text((100, 200), text_to_print, fill="white", font=font)
        
        img.save("final_post.jpg")
        print("Success! Image created.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_post()
