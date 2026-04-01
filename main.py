import requests
from PIL import Image, ImageDraw, ImageFont
import os

API_KEY = os.getenv('FOOTBALL_API_KEY')
# רשימת ליגות שבד"כ פתוחות בחינם
LEAGUES = ['PL', 'PD', 'BL1', 'SA', 'FL1', 'CL']

headers = { 'X-Auth-Token': API_KEY }

def create_post():
    print("Starting script...")
    for league in LEAGUES:
        url = f"https://api.football-data.org/v4/competitions/{league}/matches?status=FINISHED"
        try:
            print(f"Checking {league}...")
            response = requests.get(url, headers=headers)
            data = response.json()
            
            if 'matches' in data and len(data['matches']) > 0:
                match = data['matches'][-1]
                home = match['homeTeam']['shortName']
                away = match['awayTeam']['shortName']
                score = f"{match['score']['fullTime']['home']} - {match['score']['fullTime']['away']}"
                
                text = f"{home} {score} {away}"
                print(f"Match found: {text}")

                img = Image.open("background.jpg")
                draw = ImageDraw.Draw(img)
                font = ImageFont.load_default()
                draw.text((150, 250), text, fill="white", font=font)
                
                img.save("final_post.jpg")
                print("Image created successfully!")
                return # עוצרים אחרי שמצאנו משחק אחד
        except Exception as e:
            print(f"Error in {league}: {e}")

if __name__ == "__main__":
    create_post()
