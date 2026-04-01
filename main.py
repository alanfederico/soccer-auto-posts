import requests
from PIL import Image, ImageDraw, ImageFont
import os

# הגדרות football-data.org
API_KEY = os.getenv('FOOTBALL_API_KEY')
# כאן בחרתי להביא משחקים מהליגה האנגלית (PL) כדוגמה, אפשר לשנות לכל ליגה
URL = "https://api.football-data.org/v4/competitions/PL/matches?status=FINISHED"

headers = { 'X-Auth-Token': API_KEY }

def create_post():
    try:
        response = requests.get(URL, headers=headers)
        data = response.json()
        
        # לוקחים את המשחק האחרון שהסתיים
        match = data['matches'][-1] 
        home_team = match['homeTeam']['shortName']
        away_team = match['awayTeam']['shortName']
        score = f"{match['score']['fullTime']['home']} - {match['score']['fullTime']['away']}"
        
        text_to_print = f"{home_team} {score} {away_team}"

        # יצירת התמונה
        img = Image.open("background.jpg")
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        
        # מיקום הטקסט (כאן תצטרך להתאים למרכז הרקע שלך)
        draw.text((150, 200), text_to_print, fill="white", font=font)
        
        img.save("final_post.jpg")
        print(f"Post created: {text_to_print}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_post()
