import requests
from PIL import Image, ImageDraw, ImageFont, ImageChops
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
        img.thumbnail((70, 70))
        return img
    except:
        return None

def create_gradient_mask(w, h):
    # יוצר מסיכה שחורה שדועכת בצדדים (נעלמת ב-0 ו-W)
    mask = Image.new('L', (w, h), 0)
    draw = ImageDraw.Draw(mask)
    for i in range(w):
        # חישוב שקיפות: חזק במרכז (255) וחלש בקצוות (0)
        opacity = int(255 * (1 - abs(i - w/2) / (w/2))**2) 
        draw.line((i, 0, i, h), fill=max(0, min(255, opacity)))
    return mask

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
                
                # 1. יצירת הרקע השחור המטושטש (Gradient)
                shape_h = 550
                overlay = Image.new('RGBA', (W, shape_h), (0, 0, 0, 180))
                mask = create_gradient_mask(W, shape_h)
                img.paste(overlay, (0, int(H/2 - shape_h/2)), mask)
                
                draw = ImageDraw.Draw(img)
                font_main = ImageFont.truetype("font.ttf", 42)
                font_score = ImageFont.truetype("font.ttf", 60)

                y_start = H/2 - 180
                for i, m in enumerate(matches):
                    y_offset = y_start + (i * 180)
                    home = m['homeTeam']['shortName'].upper()
                    away = m['awayTeam']['shortName'].upper()
                    score = f"{m['score']['fullTime']['home']}  -  {m['score']['fullTime']['away']}"
                    
                    # לוגואים
                    logo_h = get_logo(m['homeTeam'].get('crest'))
                    logo_a = get_logo(m['awayTeam'].get('crest'))
                    if logo_h: img.paste(logo_h, (int(W*0.15), int(y_offset - 35)), logo_h)
                    if logo_a: img.paste(logo_a, (int(W*0.77), int(y_offset - 35)), logo_a)
                    
                    # טקסט
                    draw.text((W*0.32, y_offset), home, fill="white", font=font_main, anchor="mm")
                    draw.text((W*0.5, y_offset), score, fill="white", font=font_score, anchor="mm")
                    draw.text((W*0.68, y_offset), away, fill="white", font=font_main, anchor="mm")
                    
                    # 2. קווי הפרדה לבנים (כמו בדוגמה)
                    if i < len(matches) - 1:
                        line_y = y_offset + 90
                        draw.line([W*0.1, line_y, W*0.9, line_y], fill=(255, 255, 255, 100), width=2)

                img.convert("RGB").save("final_post.jpg")
                print("Final polished design created!")
                return
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    create_post()
