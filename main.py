import requests
from PIL import Image, ImageDraw, ImageFont
import os

API_KEY = os.getenv('FOOTBALL_API_KEY')
LEAGUES = ['PL', 'PD', 'BL1', 'SA', 'FL1', 'CL']
headers = { 'X-Auth-Token': API_KEY }

def create_post():
    for league in LEAGUES:
        url = f"https://api.football-data.org/v4/competitions/{league}/matches?status=FINISHED"
        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            
            if 'matches' in data and len(data['matches']) >= 3:
                # לוקחים את 3 המשחקים האחרונים
                matches_to_show = data['matches'][-3:]
                
                img = Image.open("background.jpg").convert("RGBA")
                overlay = Image.new('RGBA', img.size, (0,0,0,0))
                draw = ImageDraw.Draw(overlay)
                W, H = img.size
                
                # טעינת הפונט (נשתמש בגודל 45 לפרטים ו-60 לתוצאה)
                font_main = ImageFont.truetype("font.ttf", 55)
                font_score = ImageFont.truetype("font.ttf", 70)

                # יצירת המלבן השחור החצי שקוף במרכז
                shape_h = 500
                draw.rectangle([W*0.1, H/2 - shape_h/2, W*0.9, H/2 + shape_h/2], fill=(0,0,0,160))
                
                img = Image.alpha_composite(img, overlay).convert("RGB")
                draw = ImageDraw.Draw(img)

                # כתיבת 3 המשחקים
                y_offset = H/2 - 180
                for m in matches_to_show:
                    home = m['homeTeam']['shortName'].upper()
                    away = m['awayTeam']['shortName'].upper()
                    score = f"{m['score']['fullTime']['home']} - {m['score']['fullTime']['away']}"
                    
                    # מרכוז טקסט
                    draw.text((W*0.25, y_offset), home, fill="white", font=font_main, anchor="mm")
                    draw.text((W*0.5, y_offset), score, fill="white", font=font_score, anchor="mm")
                    draw.text((W*0.75, y_offset), away, fill="white", font=font_main, anchor="mm")
                    
                    y_offset += 150 # רווח בין משחק למשחק
                
                img.save("final_post.jpg")
                print("New design created with 3 matches!")
                return
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    create_post()
