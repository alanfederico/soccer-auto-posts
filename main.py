import requests
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

# משיכת המפתח מה-Secret שיצרנו
API_KEY = os.getenv('FOOTBALL_API_KEY')
API_HOST = "api-football-v1.p.rapidapi.com"

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

# תאריך של היום
today = datetime.now().strftime('%Y-%m-%d')
# סטטוס FT אומר משחקים שהסתיימו
querystring = {"date": today, "status": "FT"} 

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST
}

def create_post():
    print(f"Starting script for {today}...")
    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()

        # בדיקה אם יש תוצאות
        if not data.get('response') or len(data['response']) == 0:
            print("No finished matches found yet. Try again later today.")
            return

        # לוקחים את המשחק הראשון שמצאנו
        match = data['response'][0]
        home = match['teams']['home']['name']
        away = match['teams']['away']['name']
        score_home = match['goals']['home']
        score_away = match['goals']['away']
        league = match['league']['name']

        text_to_print = f"{league}\n{home} {score_home} - {score_away} {away}"
        print(f"Match found: {text_to_print}")

        # עיבוד התמונה
        img = Image.open("background.jpg")
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        
        # כתיבת הטקסט - מיקום (100, 100)
        draw.multiline_text((100, 100), text_to_print, fill="white", font=font)
        
        img.save("final_post.jpg")
        print("Success! final_post.jpg was created.")

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    create_post()
