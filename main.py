import requests
from PIL import Image, ImageDraw, ImageFont
import os

API_KEY = os.getenv('FOOTBALL_API_KEY')
# נשתמש כרגע בליגה האנגלית (PL)
URL = "https://api.football-data.org/v4/competitions/PL/matches?status=FINISHED"

headers = { 'X-Auth-Token': API_KEY }

def create_post():
    print("Starting the script...")
    try:
        response = requests.get(URL, headers=headers)
        data = response.json()
        
        if 'matches' not in data or len(data['matches']) == 0:
            print("No matches found! Checking why...")
            print(f"API Response: {data}")
            return

        # לוקחים את המשחק האחרון
        match = data['matches'][-1] 
        home = match['homeTeam']['shortName']
        away = match['awayTeam']['shortName']
        score_home = match['score']['fullTime']['home']
        score_away = match['score']['fullTime']['away']
        
        text_to_print = f"{home} {score_home} - {score_away} {away}"
        print(f"Match found: {text_to_print}")

        # יצירת התמונה
        if not os.path.exists("background.jpg"):
            print("Error: background.jpg not found in the folder!")
            return
            
        img = Image.open("background.jpg")
        draw = ImageDraw.Draw(img)
        
        # שימוש בפונט ברירת מחדל
        font = ImageFont.load_default()
        
        # כתיבת הטקסט
        draw.text((50, 50), text_to_print, fill="white", font=font)
        
        # שמירה
        img.save("final_post.jpg")
        print("Success: final_post.jpg has been created!")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    create_post()
