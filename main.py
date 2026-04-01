import requests
from PIL import Image, ImageDraw, ImageFont
import os

API_KEY = os.getenv('FOOTBALL_API_KEY')
# ניסיון למשוך משחקים מליגת האלופות (CL) או מהליגה הברזילאית (BSA)
# הליגות החינמיות הן: PL, PD, BL1, SA, FL1, CL, BSA, ELC, PPL, DED
LEAGUES = ['CL', 'BSA', 'PL', 'PD']

headers = { 'X-Auth-Token': API_KEY }

def create_post():
    print("Starting the script...")
    match_found = False
    
    for league in LEAGUES:
        if match_found: break
        
        print(f"Checking league: {league}")
        url = f"https://api.football-data.org/v4/competitions/{league}/matches?status=FINISHED"
        
        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            
            if 'matches' in data and len(data['matches']) > 0:
                match = data['matches'][-1] # המשחק האחרון שהסתיים
                home = match['homeTeam']['shortName']
                away = match['awayTeam']['shortName']
                score_home = match['score']['fullTime']['home']
                score_away = match['score']['fullTime']['away']
                
                text_to_print = f"{home} {score_home} - {score_away} {away}"
                print(f"Found match in {league}: {text_to_print}")
                
                # יצירת התמונה
                img = Image.open("background.jpg")
                draw = ImageDraw.Draw(img)
                font = ImageFont.load_default()
                draw.text((100, 200), text_to_print, fill="white", font=font)
                
                img.save("final_post.jpg")
                print("Success: final_post.jpg created!")
                match_found = True
            else:
                print(f"No finished matches in {league}")
                
        except Exception as e:
            print(f"Error in {league}: {e}")

    if not match_found:
        print("Could not find any matches in the allowed free leagues.")

if __name__ == "__main__":
    create_post()
