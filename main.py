import requests
from PIL import Image, ImageDraw, ImageFont
import os
from io import BytesIO
from datetime import datetime

API_KEY = os.getenv('FOOTBALL_API_KEY')
# סדר הליגות לפי הבקשה שלך
LEAGUES = ['PD', 'PL', 'SA', 'BL1', 'FL1']
headers = { 'X-Auth-Token': API_KEY }

# מילון הקבוצות המעודכן לפי הבקשה שלך
MY_TEAMS = {
    'PL': ['Man City', 'Arsenal', 'Liverpool', 'Chelsea', 'Man United'],
    'PD': ['Real Madrid', 'Barcelona', 'Girona', 'Atleti', 'Athletic Club'],
    'BL1': ['Leverkusen', 'Bayern', 'Dortmund', 'RB Leipzig'],
    'SA': ['Inter', 'Milan', 'Juventus', 'AS Roma', 'Napoli'],
    'FL1': ['PSG', 'Monaco', 'Marseille']
}

def get_img(url, size=(100, 100)):
    try:
        if not url or url.endswith('.svg'): return None
        response = requests.get(url, timeout=5)
        img = Image.open(BytesIO(response.content)).convert("RGBA")
        img.thumbnail(size)
        return img
    except: return None

def draw_match_row(img, y_center, match, font_score, font_names, font_date):
    W, H = img.size
    draw = ImageDraw.Draw(img, "RGBA")
    row_h = 145
    overlay = Image.new('RGBA', (W, row_h), (0, 0, 0, 0))
    d_ov = ImageDraw.Draw(overlay)
    for x in range(W):
        opacity = int(120 * (1 - abs(x - W/2) / (W/2))**3)
        d_ov.line((x, 0, x, row_h), fill=(0, 0, 0, opacity))
    img.paste(overlay, (0, int(y_center - row_h/2)), overlay)

    home_name = match['homeTeam']['shortName'].upper()
    away_name = match['awayTeam']['shortName'].upper()
    score = f"{match['score']['fullTime']['home']} - {match['score']['fullTime']['away']}"
    date_obj = datetime.strptime(match['utcDate'].split('T')[0], '%Y-%m-%d')
    formatted_date = date_obj.strftime('%d/%m/%Y')

    logo_h = get_img(match['homeTeam'].get('crest'), (95, 95))
    logo_a = get_img(match['awayTeam'].get('crest'), (95, 95))
    left_x, right_x, center_x = W * 0.22, W * 0.78, W * 0.5

    if logo_h:
        lw, lh = logo_h.size
        img.paste(logo_h, (int(left_x - lw/2), int(y_center - 55)), logo_h)
    draw.text((left_x, y_center + 52), home_name, fill="white", font=font_names, anchor="mm")
    draw.text((center_x, y_center - 15), score, fill="white", font=font_score, anchor="mm")
    draw.text((center_x, y_center + 30), formatted_date, fill="lightgray", font=font_date, anchor="mm")
    if logo_a:
        lw, lh = logo_a.size
        img.paste(logo_a, (int(right_x - lw/2), int(y_center - 55)), logo_a)
    draw.text((right_x, y_center + 52), away_name, fill="white", font=font_names, anchor="mm")

def create_post():
    for league in LEAGUES:
        url = f"https://api.football-data.org/v4/competitions/{league}/matches?status=FINISHED"
        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            if 'matches' in data:
                # סינון לפי רשימת הקבוצות המוגדרת לכל ליגה
                league_teams = MY_TEAMS.get(league, [])
                filtered_matches = [
                    m for m in data['matches'] 
                    if m['homeTeam']['shortName'] in league_teams 
                    or m['awayTeam']['shortName'] in league_teams
                ][-15:]

                if not filtered_matches: continue

                league_logo = get_img(data['competition'].get('emblem'), (200, 200))
                chunks = [filtered_matches[i:i + 5] for i in range(0, len(filtered_matches), 5)]
                
                for idx, chunk in enumerate(chunks):
                    img = Image.open("background.jpg").convert("RGBA")
                    W, H = img.size
                    if league_logo:
                        lw, lh = league_logo.size
                        img.paste(league_logo, (int(W/2 - lw/2), 60), league_logo)

                    font_score = ImageFont.truetype("font.ttf", 75)
                    font_names = ImageFont.truetype("font.ttf", 22)
                    font_date = ImageFont.truetype("font.ttf", 18)

                    total_rows = len(chunk)
                    spacing = 155
                    start_y = (H / 2) - ((total_rows - 1) * spacing / 2) + 20

                    for i, match in enumerate(chunk):
                        draw_match_row(img, start_y + (i * spacing), match, font_score, font_names, font_date)

                    img.convert("RGB").save(f"final_{league}_{idx+1}.jpg")
                    print(f"Saved: final_{league}_{idx+1}.jpg")
        except Exception as e: print(f"Error in {league}: {e}")

if __name__ == "__main__":
    create_post()
