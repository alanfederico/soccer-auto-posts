import requests
from PIL import Image, ImageDraw, ImageFont
import os
from io import BytesIO

API_KEY = os.getenv('FOOTBALL_API_KEY')
LEAGUES = ['PL', 'PD', 'BL1', 'SA', 'FL1', 'CL']
headers = { 'X-Auth-Token': API_KEY }

def get_logo(url):
    try:
        if not url or url.endswith('.svg'): return None
        response = requests.get(url, timeout=5)
        img = Image.open(BytesIO(response.content)).convert("RGBA")
        img.thumbnail((110, 110)) # הגדלתי מעט את הלוגו כדי שיראה טוב
        return img
    except:
        return None

def create_post():
    for league in LEAGUES:
        url = f"https://api.football-data.org/v4/competitions/{league}/matches?status=FINISHED"
        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            if 'matches' in data and len(data['matches']) >= 3:
                matches = data['matches'][-3:]
                img = Image.open("background.jpg").convert("RGBA")
                W, H = img.size
                
                # 1. יצירת הרקע השחור המטושטש (החלשתי את השקיפות)
                shape_h = 600
                overlay = Image.new('RGBA', img.size, (0,0,0,0))
                draw_ov = ImageDraw.Draw(overlay)
                # רקע אחיד אבל חלש (שקיפות 100 במקום 180)
                draw_ov.rectangle([W*0.05, H/2 - shape_h/2, W*0.95, H/2 + shape_h/2], fill=(0,0,0,100))
                img = Image.alpha_composite(img, overlay)
                
                draw = ImageDraw.Draw(img)
                # גדלי פונט חדשים: תוצאה גדולה, שמות קטנים
                font_score = ImageFont.truetype("font.ttf", 85)
                font_names = ImageFont.truetype("font.ttf", 25)

                y_start = H/2 - 200
                for i, m in enumerate(matches):
                    y_offset = y_start + (i * 200)
                    home = m['homeTeam']['shortName'].upper()
                    away = m['awayTeam']['shortName'].upper()
                    score = f"{m['score']['fullTime']['home']}  -  {m['score']['fullTime']['away']}"
                    
                    # לוגואים
                    logo_h = get_logo(m['homeTeam'].get('crest'))
                    logo_a = get_logo(m['awayTeam'].get('crest'))
                    
                    # מיקום וסידור: לוגו למעלה, שם מתחת
                    if logo_h: img.paste(logo_h, (int(W*0.18), int(y_offset - 90)), logo_h)
                    if logo_a: img.paste(logo_a, (int(W*0.68), int(y_offset - 90)), logo_a)
                    
                    # שמות מתחת ללוגו
                    draw.text((W*0.25, y_offset + 50), home, fill="white", font=font_names, anchor="mm")
                    draw.text((W*0.75, y_offset + 50), away, fill="white", font=font_names, anchor="mm")
                    
                    # תוצאה גדולה וממורכזת
                    draw.text((W*0.5, y_offset - 20), score, fill="white", font=font_score, anchor="mm")
                    
                    # 2. קווי הפרדה עדינים מאוד
                    if i < len(matches) - 1:
                        line_y = y_offset + 100
                        draw.line([W*0.1, line_y, W*0.9, line_y], fill=(255, 255, 255, 40), width=2)

                img.convert("RGB").save("final_post.jpg")
                print("Polished design with name-under-logo!")
                return
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    create_post()
