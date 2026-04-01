import requests
from PIL import Image, ImageDraw, ImageFont
import os
from io import BytesIO
from datetime import datetime

API_KEY = os.getenv('FOOTBALL_API_KEY')
LEAGUES = ['PL', 'PD', 'BL1', 'SA', 'FL1', 'CL']
headers = { 'X-Auth-Token': API_KEY }

def get_logo(url):
    try:
        if not url or url.endswith('.svg'): return None
        response = requests.get(url, timeout=5)
        img = Image.open(BytesIO(response.content)).convert("RGBA")
        img.thumbnail((100, 100)) 
        return img
    except:
        return None

def draw_match_row(img, y_center, match, font_score, font_names, font_date):
    W, H = img.size
    draw = ImageDraw.Draw(img, "RGBA")
    
    # 1. יצירת מלבן שחור עם פייד (Gradient) לכל שורה
    row_h = 160
    overlay = Image.new('RGBA', (W, row_h), (0, 0, 0, 0))
    d_ov = ImageDraw.Draw(overlay)
    for x in range(W):
        # חישוב שקיפות - חזק במרכז (140) ודועך לאפס בצדדים
        opacity = int(140 * (1 - abs(x - W/2) / (W/2))**3)
        d_ov.line((x, 0, x, row_h), fill=(0, 0, 0, opacity))
    img.paste(overlay, (0, int(y_center - row_h/2)), overlay)

    # 2. נתונים מה-API
    home_name = match['homeTeam']['shortName'].upper()
    away_name = match['awayTeam']['shortName'].upper()
    score = f"{match['score']['fullTime']['home']} - {match['score']['fullTime']['away']}"
    
    # פורמט תאריך (DD/MM/YYYY)
    raw_date = match['utcDate'].split('T')[0]
    date_obj = datetime.strptime(raw_date, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%d/%m/%Y')

    # 3. לוגואים
    logo_h = get_logo(match['homeTeam'].get('crest'))
    logo_a = get_logo(match['awayTeam'].get('crest'))

    # מיקומים אופקיים קבועים
    left_side = W * 0.20
    right_side = W * 0.80
    center = W * 0.5

    # ציור צד שמאל (בית)
    if logo_h:
        img.paste(logo_h, (int(left_side - 50), int(y_center - 70)), logo_h)
    draw.text((left_side, y_center + 45), home_name, fill="white", font=font_names, anchor="mm")

    # ציור מרכז (תוצאה ותאריך)
    draw.text((center, y_center - 15), score, fill="white", font=font_score, anchor="mm")
    draw.text((center, y_center + 35), formatted_date, fill="lightgray", font=font_date, anchor="mm")

    # ציור צד ימין (חוץ)
    if logo_a:
        img.paste(logo_a, (int(right_side - 50), int(y_center - 70)), logo_a)
    draw.text((right_side, y_center + 45), away_name, fill="white", font=font_names, anchor="mm")

def create_post():
    for league in LEAGUES:
        url = f"https://api.football-data.org/v4/competitions/{league}/matches?status=FINISHED"
        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            if 'matches' in data and len(data['matches']) >= 2:
                matches = data['matches'][-2:] # לוקחים 2 משחקים כמו בדוגמה 555
                
                img = Image.open("background.jpg").convert("RGBA")
                W, H = img.size
                
                # פונטים
                font_score = ImageFont.truetype("font.ttf", 80)
                font_names = ImageFont.truetype("font.ttf", 28)
                font_date = ImageFont.truetype("font.ttf", 20)

                # ציור השורות
                draw_match_row(img, H*0.45, matches[0], font_score, font_names, font_date)
                draw_match_row(img, H*0.62, matches[1], font_score, font_names, font_date)

                img.convert("RGB").save("final_post.jpg")
                print("New dynamic layout created!")
                return
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    create_post()
